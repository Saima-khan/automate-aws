import boto3
import click
from bucket import BucketManager

session = boto3.Session(profile_name = 'pythonAutomation')
bucket_manager = BucketManager(session)

@click.group(invoke_without_command = True)
def cli():
    """Webotron will add websites to AWS"""
    print("Yeah. I will always run. I am grouping all commands.")


@cli.command('list-bucket')
def list_buckets():
    """List all the bucktes in s3"""
    for bucket in bucket_manager.all_buckets():
        print(bucket.name)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List all objects in a bucket"""
    print('{0} bucket contains: '.format(bucket_manager.get_bucket_name(bucket)))
    for obj in bucket_manager.all_objects(bucket):
        print(obj.key)


@cli.command('configure-s3-bucket')
@click.argument('bucket')
def configure_s3_bucket(bucket):
    """Configuring a bucket for website"""
    bucket_name = bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(bucket_name)
    bucket_manager.configure_website(bucket_name)
    return




@cli.command('sync')
@click.argument('pathname',type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname,bucket):
    """Syncs contents of PATHNAME to BUCKET"""
    bucket_manager.sync(pathname,bucket)



if __name__ == "__main__":
    cli()
