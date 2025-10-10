"""
Upload media files to S3
Run with: python upload_to_s3.py
"""
import os
import boto3
from pathlib import Path

# Get credentials from environment or set them here temporarily
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', input('Enter AWS_ACCESS_KEY_ID: '))
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', input('Enter AWS_SECRET_ACCESS_KEY: '))
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', input('Enter bucket name: '))
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_S3_REGION_NAME
)

def upload_directory(local_directory, s3_prefix=''):
    """Upload all files in directory to S3"""
    local_path = Path(local_directory)

    if not local_path.exists():
        print(f"Directory {local_directory} not found!")
        return

    files_uploaded = 0

    for file_path in local_path.rglob('*'):
        if file_path.is_file():
            # Get relative path from media directory
            relative_path = file_path.relative_to(local_path.parent)
            s3_key = str(relative_path).replace('\\', '/')

            # Determine content type
            content_type = 'application/octet-stream'
            if file_path.suffix.lower() in ['.jpg', '.jpeg']:
                content_type = 'image/jpeg'
            elif file_path.suffix.lower() == '.png':
                content_type = 'image/png'
            elif file_path.suffix.lower() == '.gif':
                content_type = 'image/gif'
            elif file_path.suffix.lower() == '.mp4':
                content_type = 'video/mp4'

            print(f"Uploading {s3_key}...")

            try:
                s3_client.upload_file(
                    str(file_path),
                    AWS_STORAGE_BUCKET_NAME,
                    s3_key,
                    ExtraArgs={
                        'ContentType': content_type,
                        'ACL': 'public-read'
                    }
                )
                files_uploaded += 1
                print(f"  ✓ Uploaded: {s3_key}")
            except Exception as e:
                print(f"  ✗ Error uploading {s3_key}: {e}")

    print(f"\n✅ Uploaded {files_uploaded} files to S3!")
    print(f"Bucket: {AWS_STORAGE_BUCKET_NAME}")
    print(f"Files are accessible at: https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/")

if __name__ == '__main__':
    media_dir = Path(__file__).parent / 'media'
    print(f"Uploading files from: {media_dir}")
    upload_directory(media_dir)
