import boto3
from app.config import AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_BUCKET

def upload_file(file, user_id, data_id):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    file_key = f"{user_id}/{data_id}/{file.filename}"
    s3_client.upload_fileobj(file.file, S3_BUCKET, file_key)
    return file_key

def get_file_url(file_key):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    return s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': S3_BUCKET, 'Key': file_key},
        ExpiresIn=3600
    )