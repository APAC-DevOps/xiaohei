# Upload local objects to s3 bucket. if remote S3 bucket does not exist, it would be created.
import os
import sys
import boto3
from botocore.client import ClientError
import logging

def console_logger():
    console_logger_extra = { 'line_begin': 'JIANHUA WU', 'prefix_padding': '=====', 'suffix_padding': '=====' }
    console_logger_handler = logging.StreamHandler()
    console_logger_formatter = logging.Formatter('%(asctime)s %(message)s')
    console_logger_handler.setFormatter(console_logger_formatter)
    console_logger = logging.getLogger()
    console_logger.setLevel(logging.INFO)
    console_logger.addHandler(console_logger_handler)

def s3_upload(Bucket, LocalPath, Region):
    console_logger()
    abs_local_path = os.path.abspath(LocalPath)
    s3 = boto3.resource('s3')
    try:
        s3.meta.client.head_bucket(Bucket=Bucket)
        logging.info("The S3 Bucket " + Bucket + " Exists!")
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 403:
            sys.exit("Private Bucket. Forbidden Access!")
        elif error_code == 404:
            logging.info("Bucket Does Not Exist!")
            s3_client = boto3.client('s3')
            s3_client.create_bucket(
                ACL='private',
                Bucket=Bucket,
                CreateBucketConfiguration={
                    'LocationConstraint': Region
                }
            )
            logging.info("Bucket " + Bucket + "Has Been Created!")

    logging.info("Uploading objects to the S3 bucket " + Bucket)
    for base_dir, dirs, file_names in os.walk(abs_local_path, topdown=True):
        # filter out hidden files and directories
        file_names = [ file_name for file_name in file_names if not file_name[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for local_file_name in file_names:
            local_file_name = os.path.join(base_dir, local_file_name)
            remote_file_name = os.path.join(base_dir, local_file_name)[len(abs_local_path) + 1:]
            s3.meta.client.upload_file(
                local_file_name,
                Bucket,
                remote_file_name
                )
            logging.info('Uploaded the object:' + local_file_name)
    logging.info("Done Objects Upload")
