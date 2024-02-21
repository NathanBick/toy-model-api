import boto3
from botocore import UNSIGNED
from botocore.config import Config

bucket_name = "cfpb-hmda-public"
prefix = "prod/dynamic-data/"  # If you want to list files under a specific directory, adjust the prefix accordingly

# Create a session without credentials
s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

#"https://s3.amazonaws.com/cfpb-hmda-public/prod/dynamic-data/2022/2022_lar.zip"

def list_files(bucket, prefix):
    """List files in specific S3 URL"""
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix)

    files = []

    for page in page_iterator:
        if "Contents" in page:
            for obj in page["Contents"]:
                print(obj["Key"])
                files.append(obj["Key"])

    return files
    

files = list_files(bucket_name, prefix)
