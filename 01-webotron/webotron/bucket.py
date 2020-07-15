"""Classes for S3 Bucket."""
import mimetypes
from pathlib import Path
import util
from hashlib import md5
from functools import reduce
import boto3

class BucketManager:
    """Class to Manage Bucket."""

    CHUNK_SIZE = 8388608
    def __init__(self,session):
        """Create a BucketManger Obect."""
        self.s3 = session.resource('s3')
        self.manifest = {}
        self.transfer_config = boto3.s3.transfer.TransferConfig(
            multipart_chunksize = self.CHUNK_SIZE,
            multipart_threshold = self.CHUNK_SIZE
        )

    def get_region_name(self,bucket):
        """Get the bucket's region"""
        bucket_location = self.s3.meta.client.get_bucket_location(Bucket=bucket.name)
        return bucket_location["LocationConstraint"] or 'us-east-1'

    def get_bucket_url(self,bucket):
        """Get the url for s3 bucket"""
        return "http://{}.{}".format(bucket.name,util.get_endpoint(self.get_region_name(bucket)).host)

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

    def upload_file(self,path,key,bucket):
        """Uploads file to s3 bucket."""
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'

        etag = self.generate_etag(path)
        if self.manifest.get(key, ' ') == etag:
            print("Skipping {}, etags match".format(key))
            return

        return bucket.upload_file(path,key,
                    ExtraArgs={
                    'ContentType' : content_type},
                    Config=self.transfer_config
                    )

    @staticmethod
    def hash_data(data):
        hash = md5()
        hash.update(data)

        return hash

    def generate_etag(self,path):
        """Generates the etag for a file"""
        hashes = []

        with open(path,'rb') as f:
            while True:
                data = f.read(self.CHUNK_SIZE)
                if not data:
                    break

                hashes.append(self.hash_data(data))
            if not hashes:
                return
            elif len(hashes) == 1:
                return '"{}"'.format(hashes[0].hexdigest())
            else:
                digests = (h.digest() for h in hashes)
                hash = self.hash_data(reduce(lambda x, y: x + y, digests))
                return '"{}-{}"'.format(hash.hexdigest(), len(hashes))


    def load_manifest(self,bucket):
        paginator = self.s3.meta.client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket.name):
            for obj in page.get('Contents',[]):
                self.manifest[obj['Key']]=obj['ETag']


    def sync(self,pathname,bucket):
        """Syncs the file to bucket."""
        bucket_name = self.s3.Bucket(bucket)
        self.load_manifest(bucket_name)

        root = Path(pathname).expanduser().resolve()
        def handle_directory(target):
            for path in target.iterdir():
                if path.is_dir(): handle_directory(path)
                if path.is_file(): self.upload_file(str(path),str(path.relative_to(root)),bucket_name)
        handle_directory(root)
