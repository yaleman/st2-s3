#!/usr/bin/env python

from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)

from client import minio_client

if __name__ != '__main__':
    from st2common.content import utils
    from st2common.runners.base_action import Action

class S3_list_objects(Action):
    def run(self, endpoint_secure=True, endpoint=None, access_key=None, secret_key=None, bucket=None):
        """ lists objects in a bucket """

        # Initialize minioClient with an endpoint and access/secret keys.
        success, minioClient = minio_client(self, endpoint=endpoint, endpoint_secure=endpoint_secure, access_key=access_key, secret_key=secret_key)

        if not success:
            return (False, minioClient)

        try:
            if not minioClient.bucket_exists(bucket):
                return (False, "Bucket {} doesn't exists".format(bucket))
            else:
                return (True, minioClient.list_objects(bucket))
        except ResponseError as err:
            return (False, err)