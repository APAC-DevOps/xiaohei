import os
import sys
import boto3
from botocore.client import ClientError
import argparse
import logging

# Upload local objects to s3 bucket
# Usage: python3 s3.py --S3Bucket "BucketName"
parser = argparse.ArgumentParser(
    description='parse option arguments passed to this script',
    epilog='you can write to wujianhua@outlook.jp for help',
    prefix_chars='-'
    )

parser.add_argument('--S3Bucket', required = True, help = 'the name of your S3 Bucket for DevOps Code')
parser.add_argument('--LocalPath', default = '.', help = 'the path to your local objects')
parsed_argu = parser.parse_args(sys.argv[1:])
s3_bucket_name = parsed_argu.S3Bucket
local_path = parsed_argu.LocalPath
abs_local_path = os.path.abspath(local_path)
s3 = boto3.resource('s3')
remote_dir_path = ''

def console_logger():
    console_logger_extra = { 'line_begin': 'JIANHUA WU', 'prefix_padding': '=====', 'suffix_padding': '=====' }
    console_logger_handler = logging.StreamHandler()
    console_logger_formatter = logging.Formatter('%(asctime)s %(message)s')
    console_logger_handler.setFormatter(console_logger_formatter)
    console_logger = logging.getLogger()
    console_logger.setLevel(logging.INFO)
    console_logger.addHandler(console_logger_handler)

def s3_upload():
    try:
        s3.meta.client.head_bucket(Bucket=s3_bucket_name)
        logging.info("The S3 Bucket " + s3_bucket_name + " Exists!")
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 403:
            sys.exit("Private Bucket. Forbidden Access!")
        elif error_code == 404:
            logging.info("Bucket Does Not Exist!")
            s3_client = boto3.client('s3')
            s3_client.create_bucket(
                ACL='private',
                Bucket=s3_bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint': 'ap-southeast-2'
                }
            )
            logging.info("Bucket " + s3_bucket_name + "Has Been Created!")

    logging.info("Uploading objects to the S3 bucket " + s3_bucket_name)
    for base_dir, dirs, file_names in os.walk(abs_local_path, topdown=True):
        # filter out hidden files and directories
        file_names = [ file_name for file_name in file_names if not file_name[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for local_file_name in file_names:
            local_file_name = os.path.join(base_dir, local_file_name)
            remote_file_name = os.path.join(base_dir, local_file_name)[len(abs_local_path) + 1:]
            s3.meta.client.upload_file(
                local_file_name,
                s3_bucket_name,
                remote_file_name
                )
            logging.info('Uploaded the object:' + local_file_name)

    logging.info("Done Objects Upload")

if __name__ == "__main__":
    console_logger()
    s3_upload()
