from botocore.retries import bucket
from django.http.response import HttpResponse
import boto3
import os

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

def hash(content):
    return content

def handleNewUser(request):
    username = request.GET.get("username", None)
    password = request.GET.get("password", None)
    if not username or not password:
        return HttpResponse("Username and password are needed")

    byte_hashed_password = hash(password).encode()
    try:
        s3.put_object(Body=byte_hashed_password, Key=username, Bucket=BUCKET_NAME)
    except:
        return HttpResponse("Create user failed")

    return HttpResponse("Done")

def handleLogin(request):
    username = request.GET.get("username", None)
    password = request.GET.get("password", None)
    if not username or not password:
        return HttpResponse("Username and password are required")
    
    byte_hashed_password = None
    try:
        byte_hashed_password = s3.get_object(Bucket=BUCKET_NAME, Key=username)['Body'].read()
    except s3.exceptions.NoSuchKey:
        return HttpResponse("Username not found")
    except:
        return HttpResponse("Login failed")

    if hash(password).encode() == byte_hashed_password:
        return HttpResponse("Done")
    return HttpResponse("Password is invalid")

def handleUpdatePassword(request):
    username = request.GET.get("username", None)
    old_password = request.GET.get("old_password", None)
    new_password = request.GET.get("new_password", None)
    if not username or not old_password or not new_password:
        return HttpResponse("Username, old password and new password are required")

    byte_hashed_old_password = None
    try:
        byte_hashed_old_password = s3.get_object(Bucket=BUCKET_NAME, Key=username)['Body'].read()
    except s3.exceptions.NoSuchKey:
        return HttpResponse("Username not found")
    except:
        return HttpResponse("Update password failed")
    
    if hash(old_password).encode() != byte_hashed_old_password:
        return HttpResponse("Password doesn't match")

    # re-upload file with hashed new password as file content
    byte_hashed_new_password = hash(new_password).encode()
    s3.put_object(Body=byte_hashed_new_password, Key=username, Bucket=BUCKET_NAME)

    return HttpResponse("Done")

def index(request):
    command = request.GET.get('command', None)
    if not command : return HttpResponse("Please enter a command")

    if command == 'newuser': return handleNewUser(request)
    elif command == 'login': return handleLogin(request)
    elif command == 'updatepassword': return handleUpdatePassword(request)
    else: return HttpResponse("Invalid command")
