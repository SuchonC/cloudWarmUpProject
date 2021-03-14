from django.http import JsonResponse
import boto3
import os
import hashlib
import base64

if not "AWS_ACCESS_KEY_ID" in os.environ:
    print("Environment AWS_ACCESS_KEY_ID not found")
    exit()
if not "AWS_SECRET_ACCESS_KEY" in os.environ:
    print("Environment AWS_SECRET_ACCESS_KEY not found")
    exit()

s3 = boto3.client(
    's3',
    aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
)

BUCKET_NAME = "s3warmup"

def hash(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        'sha512',  # The hash digest algorithm for HMAC
        password.encode('utf-8'),  # Convert the password to bytes
        salt,  # Provide the salt
        100000  # Iterations
    )
    return base64.b64encode(salt + key).decode('utf-8')

def verify_password(hashed_password, password):
    hashed_password = base64.b64decode(hashed_password.encode('utf-8'))
    salt = hashed_password[:32]
    key = hashed_password[32:]
    new_key = hashlib.pbkdf2_hmac(
        'sha512',  # The hash digest algorithm for HMAC
        password.encode('utf-8'),  # Convert the password to bytes
        salt,  # Provide the salt
        100000  # Iterations
    )
    return new_key == key

def getJson(message, code=200):
    return JsonResponse({
        "message": message
    }, status = code)

def handleNewUser(request):
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)
    if not username or not password:
        return getJson("Username and password are required")

    try:
        s3.head_object(Bucket=BUCKET_NAME, Key=username)
    except s3.exceptions.ClientError: # username not found -> available to user
        byte_hashed_password = hash(password).encode()

        try:
            s3.put_object(Body=byte_hashed_password, Key=username, Bucket=BUCKET_NAME)
        except:
            return getJson("Create account failed")

        return getJson("Create account successfully!")
    
    return getJson("This username is already existed!")

def handleLogin(request):
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)
    if not username or not password:
        return getJson("Username and password are required")
    
    byte_hashed_password = None
    try:
        byte_hashed_password = s3.get_object(Bucket=BUCKET_NAME, Key=username)['Body'].read()
    except s3.exceptions.NoSuchKey:
        return getJson("Username not found or password is incorrect!")
    except:
        return getJson("Login failed")

    if verify_password(byte_hashed_password.decode(), password):
        return getJson("Login successfully!")

    return getJson("Username not found or password is incorrect!", 401)

def handleUpdatePassword(request):
    username = request.POST.get("username", None)
    old_password = request.POST.get("password", None)
    new_password = request.POST.get("new-password", None)
    if not username or not old_password or not new_password:
        return getJson("Username, password and new-password are required")

    byte_hashed_old_password = None
    try:
        byte_hashed_old_password = s3.get_object(Bucket=BUCKET_NAME, Key=username)['Body'].read()
    except s3.exceptions.NoSuchKey:
        return getJson("Username not found", 404)
    except:
        return getJson("Update password failed")

    if not verify_password(byte_hashed_old_password.decode(), old_password):
        return getJson("Password doesn't match")

    # re-upload file with hashed new password as file content
    byte_hashed_new_password = hash(new_password).encode()
    s3.put_object(Body=byte_hashed_new_password, Key=username, Bucket=BUCKET_NAME)

    return getJson("Change password successfully!")

def register(request):
    return handleNewUser(request)

def login(request):
    return handleLogin(request)

def updatePassword(request):
    return handleUpdatePassword(request)
