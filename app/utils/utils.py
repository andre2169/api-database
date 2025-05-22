import boto3
from app.config import AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_BUCKET

def delete_file(file_key: str):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY ,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    s3.delete_object(Bucket=S3_BUCKET, Key=file_key)