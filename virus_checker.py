import requests
import boto3

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

    access_key = input("Enter your AWS access key: ")
    secret_key = input("Enter your AWS secret key: ")
    session_token = input("Enter your AWS session token (if applicable, press Enter if not): ")

    # Set AWS credentials
    boto3.setup_default_session(
        aws_access_key_id=access_key if access_key else 'x',
        aws_secret_access_key=secret_key if secret_key else 'x',
        aws_session_token=session_token if session_token else ''
    )

def download_checker(bucket, object, src):
    reset_aws_credentials()
    print("\n[*]----------------------------------------------------[*]")
    print("[*]   You must log in to your AWS account to download. [*]")
    print("[*]----------------------------------------------------[*]")

            # Prompt the user to log in
    log_in_to_aws()

            # Check credentials again after logging in
    if not check_aws_credentials():
        print("[*]----------------------------------------------[*]")
        print("[*]      Failed to log in. Aborting download.    [*]")
        print("[*]----------------------------------------------[*]")
        return
    # Check the file with VirusTotal API (using API v2)
    virus_total_api_key = "f5ebbf971603fbd87384f9e197f0a010a71a15af3d02612576294e680078c0ac"
    virus_total_url = 'https://www.virustotal.com/vtapi/v2/url/report'
    virus_total_params = {
        'apikey': virus_total_api_key,
        'resource': f'https://{bucket}.s3.amazonaws.com/{object}'
    }

    virus_total_response = requests.get(virus_total_url, params=virus_total_params)
    virus_total_result = virus_total_response.json()

    # Print specific information from the VirusTotal response
    print("[*] -------------------------------- VirusTotal API Response ------------------------------- [*]\n")
    print({
        'scan_id': virus_total_result.get('scan_id'),
        'resource': virus_total_result.get('resource'),
        'url': virus_total_result.get('url'),
        'response_code': virus_total_result.get('response_code'),
        'scan_date': virus_total_result.get('scan_date'),
        'permalink': virus_total_result.get('permalink')
    })

    # Check if the file is safe
    if virus_total_result.get("positives", 0) == 0:

        # Download the file from S3
        s3 = boto3.client('s3')
        try:
            s3.download_file(bucket, object, src)
            print("\n[*]----------------------------------------------[*]")
            print(f"[*]        File {object} Downloaded!!!          [*]")
            print("[*]----------------------------------------------[*]")
        except Exception as e:
            print(f"Error downloading file to destination: {e}")
    else:
        print("\n[*]----------------------------------------------------[*]")
        print(f"[*]  File {object} is MALICIOUS. Aborting DOWNLOAD !!!   [*]")
        print("[*]------------------------------------------------------[*]")


