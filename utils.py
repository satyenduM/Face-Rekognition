import boto3
import os
import re
from botocore.exceptions import NoCredentialsError

s3 = boto3.client('s3')

def upload_file_to_storage(file):
    try:
        bucket_name = 'face-rekognition2'
        file_name = file.filename
        s3.upload_fileobj(file, bucket_name, file_name)
        return file_name
    except NoCredentialsError:
        return "Credentials not available"

def url_for_uploaded_file(file_id):
    try:
        bucket_name = 'face-rekognition2'
        url = s3.generate_presigned_url('get_object',
                                        Params={'Bucket': bucket_name, 'Key': file_id},
                                        ExpiresIn=3600)
        return url
    except NoCredentialsError:
        return "Credentials not available"
    
def extract_folder_id(drive_link):
    match = re.search(r'\/folders\/([a-zA-Z0-9_-]+)', drive_link)
    return match.group(1) if match else None
