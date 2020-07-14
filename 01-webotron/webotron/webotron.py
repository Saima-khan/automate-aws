import boto3
import click

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
def list_bucket_objects():
	"List all objects in a bucket"
	for bucket in s3.buckets.all():
		for obj in bucket.objects.all():
			print('{0} bucket contains {1}'.format(obj.bucket_name,obj.key))


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




if __name__ == "__main__":
	cli()
