""" 
AWS S3 interaction functions
"""
# import time 
# import json
# import os
# import sys
# import urllib.request
# import resource # used to monitor memory
from loguru import logger

import boto3    # Library: boto3 -- for interacting with AWS S3 buckets
import botocore # from: boto3  -- exposes boto3 error handling details
from botocore.exceptions import ClientError

S3_BUCKETS = {}
S3_CLIENT = None
S3_RESOURCE = None

# =============================================================================
#  --- INTERACT WITH AN S3 BUCKET ---
# =============================================================================
# - s3_connection (aws_region, aws_key_id, aws_key, OPTIONAL use_client) -> Boolean
# - s3_open_bucket (bucket_name, aws_region, aws_key_id, aws_key) -> Boolean
# - s3_chkdir (bucket_name, path)  -> Boolean
# - s3_chkfile (bucket_name, path) -> Boolean
# - s3_mkdir (bucket_name, path) -> Boolean
# - s3_get_file (bucket_name, file_name) -> Boolean, String
# - s3_put_file (bucket_name, file_name, content)-> Boolean
# - s3_rm_file (bucket_name, file)
# =============================================================================

# Establishes a connection to the S3 service 
# Returns True if successful (S3 service is available/reachable in the specified region and access key is accepted as valid).False otherwise.
def s3_connection(aws_region, aws_key_id, aws_key, use_client=False):
    global S3_CLIENT, S3_RESOURCE
    status = False
    s3 = None
    try:
        if S3_CLIENT is None:
            s3 = boto3.client(
                service_name="s3",
                region_name=aws_region,
                aws_access_key_id=aws_key_id,
                aws_secret_access_key=aws_key
            )
            S3_CLIENT = s3
        else:
            #  s3 = S3_CLIENT # cache it for reuse
            pass

        if S3_RESOURCE is None:
            s3 = boto3.resource(
                service_name="s3",
                region_name=aws_region,
                aws_access_key_id=aws_key_id,
                aws_secret_access_key=aws_key
            )
            S3_RESOURCE = s3 # cache it for reuse
        else:
            # s3 = S3_CLIENT # cache it for reuse
            pass
        status = True
    except Exception as error:
        logger.error(f"Unable to connect to AWS S3 service in {aws_region}. Possible invalid key or blocked communication. ({type(error).__name__}) {str(error)}")
    return status

# Opens a connect to an S3 bucket
# Returns True if successful (bucket is available and access is granted).False otherwise.
# Once a bucket is open, its object is cached until the application halts 
def s3_open_bucket(bucket_name, aws_region, aws_key_id, aws_key):
    global S3_RESOURCE, S3_BUCKETS
    status = False
    if bucket_name not in S3_BUCKETS:
        status = s3_connection(aws_region, aws_key_id, aws_key)
        if status:
            try:
                status = False
                s3_bucket = S3_RESOURCE.Bucket(bucket_name)
                status = True
                S3_BUCKETS[bucket_name] = s3_bucket # Cache the Resource connection to the Bucket
            except botocore.exceptions.ClientError as error:
                logger.warning(f"Unable to connect to {bucket_name}: {error}")
            except Exception as error:
                logger.error(f"{bucket_name} S3 bucket not found or no access. ({type(error).__name__}) {str(error)}") #  .message)

    return status 

# Checks for the existence of a folder or file on an S3 bucket
# Returns True if the folder is found
# Returns False if the folder's existence could not be determined or 
#               if there was an error creating the folder.
def s3_chkdir(bucket_name, path):
    global S3_BUCKETS
    status = False
    # status, s3 = s3_connection(aws_region, aws_key_id, aws_key, True)
    if bucket_name in S3_BUCKETS:    
        try:
            for obj in S3_BUCKETS[bucket_name].objects.all(): 
                if path == obj.key or path + "/" == obj.key:
                    # logger.info(path + " found in S3 Bucket")
                    status = True
                    break
            if not status:
                # logger.info(path + " NOT found in S3 Bucket.")
                pass
        except Exception as error:
            if type(error).__name__ == "RequestTimeTooSkewed":
                logger.error("Local host's time is too far out of sync with AWS time. ** !! This is a common problem with WSL after the local host wakes from sleep. Fix time in the local time and try again.")
            else:    
                logger.error(f"Error checking folder on S3 bucket. ({type(error).__name__}) {str(error)}")
    else:
        logger.error("Attempt to check directory on S3 bucket before opening S3 bucket.")

    return status 

# Creates a folder on an S3 bucket
# Returns True if the folder already exists or was created successfully
# Returns False if the folder's existence could not be determined or 
#               if there was an error creating the folder.
def s3_mkdir(bucket_name, path):
    global S3_BUCKETS
    status = False
    # status, s3 = s3_connection(aws_region, aws_key_id, aws_key, True)
    if bucket_name in S3_BUCKETS:
        status = s3_chkdir(bucket_name, path)
        if not status:
            try:
                S3_BUCKETS[bucket_name].put_object(Key=path + "/")
                status = True
            except Exception as error:
                logger.error(f"Problem on S3 creating {path} ({type(error).__name__}) {str(error)}")
    else:
        logger.error("Attempt to make directory on S3 bucket before opening S3 bucket.")
    
    return status

# Gets a file from a named S3 bucket
# Returns a boolean (true if successful, false if not) and actual file content
def s3_get_file(bucket_name, file_name):
    global S3_CLIENT
    status = False
    ret_value = ""
    if S3_CLIENT is not None:
        try:
            content_object = S3_CLIENT.get_object(Bucket=bucket_name, Key=file_name)
            ret_value = content_object['Body'].read().decode('utf-8')
            status = True
        except ClientError as e:
            ret_value = ""
            error_code = e.response["Error"]["Code"]
            if error_code == "AccessDenied":
                logger.error("Access Denied fetching " + file_name)
            else: # error_code == "InvalidLocationConstraint":
                logger.error(f"{e.response['Error']['Code']} fetching {file_name}: {e.response['Error']['Message']}")
        except Exception as error:
            ret_value = ""
            logger.error(f"Problem fetching {file_name} in S3 bucket {bucket_name} ({type(error).__name__}) {str(error)}")
    else:
        logger.error("Attempt to get file on S3 bucket before opening S3 bucket.")

    return status, ret_value

# Saves a file to a named S3 bucket
# Returns true if successful, false if not
def s3_put_file(bucket_name, file_name, content):
    global S3_CLIENT
    status = False
    if S3_CLIENT is not None:
        try:
            S3_CLIENT.put_object(Bucket=bucket_name, Key=file_name, Body=content, ContentEncoding="utf-8")
            status = True
        except ClientError as e:
            # ['Error']['Code'] e.g. 'EntityAlreadyExists' or 'ValidationError'
            # ['ResponseMetadata']['HTTPStatusCode'] e.g. 400
            # ['ResponseMetadata']['RequestId'] e.g. 'd2b06652-88d7-11e5-99d0-812348583a35'
            # ['Error']['Message'] e.g. "An error occurred (EntityAlreadyExists) ..."
            # ['Error']['Type'] e.g. 'Sender'
            error_code = e.response["Error"]["Code"]
            if error_code == "AccessDenied":
                logger.error("Access Denied saving " + file_name)
            else: # error_code == "InvalidLocationConstraint":
                logger.error(f"{e.response['Error']['Code']} saving {file_name}: {e.response['Error']['Message']}")
        except Exception as error:
            logger.error(f"Problem saving {file_name} in S3 bucket {bucket_name} ({type(error).__name__}) {str(error)}")
    return status

# Removes a file from an S3 bucket
# Returns true if successful, false if not
def s3_rm_file(bucket_name, file):
    logger.error("S3 Remove File not implemented (common.py/s3_rm_file)")
    return False



# =============================================================================
#  --- MAIN: Only runs if the module is executed stand-alone. ---
# =============================================================================
if __name__ == '__main__':
    # Execute when the module is not initialized from an import statement.
    logger.info("--- START ---")

    logger.info("This contains functions common the OSCAL services capability. This module does nothing when run individually.")

    logger.info("--- END ---")
