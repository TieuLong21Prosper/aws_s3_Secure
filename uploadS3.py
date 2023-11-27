"""

Function for uploading file to AWS s3 bucket.
Required fields -> file_name, bucket, object_name

"""

import os
import boto3
from botocore.exceptions import ClientError

def reset_aws_credentials():
    # Reset AWS credentials
    boto3.setup_default_session()

def check_aws_credentials():
    try:
        # Try to create an S3 client to check if credentials are available
        boto3.client('s3').list_buckets()
        return True
    except Exception as e:
        return False

def log_in_to_aws():
    # Reset AWS credentials before asking to log in again
    reset_aws_credentials()

    access_key = input("-> Enter your AWS access key: ")
    secret_key = input("-> Enter your AWS secret key: ")
    session_token = input("-> Enter your AWS session token (if applicable, press Enter if not): ")

    # Set AWS credentials
    
    boto3.setup_default_session(
        aws_access_key_id=access_key if access_key else 'x',
        aws_secret_access_key=secret_key if secret_key else 'x',
        aws_session_token=session_token if session_token else ''
    )

def upload_file(file_name, bucket, object_name=None):
    reset_aws_credentials()
    print("\n[*]----------------------------------------------------[*]")
    print("[*]    You must log in to your AWS account to upload.  [*]")
    print("[*]----------------------------------------------------[*]")

            # Prompt the user to log in
    log_in_to_aws()

            # Check credentials again after logging in
    if not check_aws_credentials():
        print("[*]----------------------------------------------[*]")
        print("[*]   Failed to log in. Aborting upload to S3.   [*]")
        print("[*]----------------------------------------------[*]")
        return
    print("* -------------------------------- PROCESSING SENDING DATA TO S3 -------------------------------- *")
    print("[*] On processing. Please wait ! ")
    if object_name is None:
        object_name = file_name

    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, str(object_name))
    print("[*]----------------------------------------------[*]")
    print("[*]          Successfully upload to S3.          [*]")
    print("[*]----------------------------------------------[*]")
    return True
