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

def handleNewUser(request):
    username = request.GET.get("username", None)
    password = request.GET.get("password", None)
    if not username or not password :
        return HttpResponse("Username and password are needed")

    hashed_password = password.encode()
    s3.put_object(Body=hashed_password, Key=username, Bucket=BUCKET_NAME)
    return HttpResponse("Done")

def index(request):
    command = request.GET.get('command', None)
    if not command : return HttpResponse("Please enter a command")
    if command == 'newuser': return handleNewUser(request)
