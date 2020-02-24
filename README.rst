=======
XIAOHEI
=======

A Jianhua WU's project

This package provides an easy way for setting up CI/CD tools on AWS and Azure.

The XIAOHEI package works on Python versions:

* 3.6.x and greater
* 3.7.x and greater
* 3.8.x and greater

-------------
Pre-requisite
-------------

* boto3
* access key & secret key of an AWS IAM user with Admin permission
* general AWS knowledge
* Azure Creds
* general Azure knowledge

----------------------
Set up AWS Environment
----------------------

The quickest way to get started is to run the ``aws configure`` command::

    $ aws configure
    AWS Access Key ID: YourAwsAccessKey
    AWS Secret Access Key: YourAwsSecretKey
    Default region name [ap-southeast-2]: ap-southeast-2
    Default output format [None]: json

For more detail, follow the link - https://github.com/aws/aws-cli/blob/develop/README.rst
