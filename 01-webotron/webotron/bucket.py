"""Classes for S3 Bucket."""
import mimetypes
from pathlib import Path


class BucketManager:
    """Class to Manage Bucket."""
    def __init__(self,session):
        """Create a BucketManger Obect."""
        self.s3 = session.resource('s3')

    def all_buckets(self):
        """Return all bucket objects."""
        return self.s3.buckets.all()

    def all_objects(self,bucket_name):
        """Return objects iterator for a particular bucket."""
        return self.s3.Bucket(bucket_name).objects.all()

    def get_bucket_name(self,bucket):
        """Return the name of a bucket."""
        return self.s3.Bucket(bucket).name

    def init_bucket(self,bucket_name):
        """Create a s3 bucket."""
        return self.s3.create_bucket(Bucket=bucket_name)

    def set_policy(self,bucket):
        """Set the policy to a bucket."""
        policy = """
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": [
                        "s3:GetObject"
                    ],
                    "Resource": [
                        "arn:aws:s3:::%s/*"
                    ]
                }
            ]
        }""" %bucket.name
        policy = policy.strip()
        pol = bucket.Policy()
        pol.put(Policy = policy)

    def configure_website(self,bucket):
        """Configure Website setting."""
        web = bucket.Website()
        web.put(WebsiteConfiguration={
            'ErrorDocument': {
                'Key': 'error.html'
            },
            'IndexDocument': {
                'Suffix': 'index.html'
            }})

    @staticmethod
    def upload_file(path,key,bucket):
        """Uploads file to s3 bucket."""
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'
        return bucket.upload_file(path,key,
                    ExtraArgs={
                    'ContentType' : content_type})

    def sync(self,pathname,bucket):
        """Syncs the file to bucket."""
        bucket_name = self.s3.Bucket(bucket)
        root = Path(pathname).expanduser().resolve()
        def handle_directory(target):
            for path in target.iterdir():
                if path.is_dir(): handle_directory(path)
                if path.is_file(): self.upload_file(str(path),str(path.relative_to(root)),bucket_name)
        handle_directory(root)
