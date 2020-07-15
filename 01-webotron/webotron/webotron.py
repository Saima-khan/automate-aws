import boto3
import click
from bucket import BucketManager

session = None
bucket_manager = None

@click.group()
@click.option('--profile', default=None,
              help="Use a given AWS profile.")
def cli(profile):
    """Webotron deploys websites to AWS."""
    global session, bucket_manager
    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile
    session = boto3.Session(**session_cfg)
    bucket_manager = BucketManager(session)


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
    print("Bucket URL: {}".format(bucket_manager.get_bucket_url(bucket_manager.s3.Bucket(bucket))))



if __name__ == "__main__":
    cli()
