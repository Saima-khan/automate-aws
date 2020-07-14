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

if __name__ == "__main__":
	cli()
