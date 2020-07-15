import boto3
import click
from pathlib import Path
import mimetypes

session = boto3.Session(profile_name = 'pythonAutomation')
s3 = session.resource('s3')

@click.group(invoke_without_command = True)
def cli():
	"Webotron will add websites to AWS"
	print("Yeah. I will always run. I am grouping all commands.")

@cli.command('list-bucket')
def list_buckets():
	"List all the bucktes in s3"
	for bucket in s3.buckets.all():
		print(bucket.name)

@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
	"List all objects in a bucket"
	b = s3.Bucket(bucket)
	print('{0} bucket contains: '.format(b.name))
	for obj in b.objects.all():
		print(obj.key)


@cli.command('configure-s3-bucket')
@click.argument('bucket')
def configure_s3_bucket(bucket):
	"Configuring a bucket for website"
	new_bucket = s3.create_bucket(Bucket=bucket)
	new_bucket.upload_file('index.html','index.html', ExtraArgs={'ContentType':'text/html'})
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
	}""" %new_bucket.name
	policy = policy.strip()
	pol = new_bucket.Policy()
	pol.put(Policy = policy)
	web = new_bucket.Website()
	web.put(WebsiteConfiguration={
        'ErrorDocument': {
            'Key': 'error.html'
        },
        'IndexDocument': {
            'Suffix': 'index.html'
        }})
	return

def upload_file(path,key,bucket):
	content_type = mimetypes.guess_type(key)[0] or 'text/plain'
	bucket.upload_file(path,key,
				ExtraArgs={
				'ContentType' : content_type})

@cli.command('sync')
@click.argument('pathname',type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname,bucket):
	"Syncs contents of PATHNAME to BUCKET"
	s3_bucket = s3.Bucket(bucket)
	root = Path(pathname).expanduser().resolve()
	def handle_directory(target):
	    for path in target.iterdir():
	        if path.is_dir(): handle_directory(path)
	        if path.is_file(): upload_file(str(path),str(path.relative_to(root)),s3_bucket)
	handle_directory(root)

if __name__ == "__main__":
	cli()
