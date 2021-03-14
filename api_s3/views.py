from django.http.response import HttpResponse
from django.shortcuts import render
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

def index(request):
    return HttpResponse("Yes, it worked")
