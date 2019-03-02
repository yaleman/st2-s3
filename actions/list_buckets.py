#!/usr/bin/env python

from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)

from client import minio_client

if __name__ != '__main__':
    from st2common.content import utils
    from st2common.runners.base_action import Action

class S3_list_buckets(Action):
    def run(self, endpoint_secure=True, endpoint=None, access_key=None, secret_key=None, bucket=None):
        """ lists available buckets """

        # Initialize minioClient with an endpoint and access/secret keys.
        success, minioClient = minio_client(self, endpoint=endpoint, endpoint_secure=endpoint_secure, access_key=access_key, secret_key=secret_key)

        if not success:
            return (False, minioClient)

        try:
            bucket_data = minioClient.list_buckets()
            bucketlist = [{'name' : bucket.name, 'creation_date' : bucket.creation_date } for bucket in bucket_data]
            return (True, bucketlist)
        except ResponseError as err:
            return (False, err)