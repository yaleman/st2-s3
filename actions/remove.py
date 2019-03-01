#!/usr/bin/env python

from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)

from client import minio_client

if __name__ != '__main__':
    from st2common.content import utils
    from st2common.runners.base_action import Action

class S3_put(Action):
    def run(self, endpoint_secure=True, endpoint=None, access_key=None, secret_key=None, filename=None, bucket=None):
        """ removes a file from a bucket """

        # Initialize minioClient with an endpoint and access/secret keys.
        success, minioClient = minio_client(self, endpoint=endpoint, endpoint_secure=endpoint_secure, access_key=access_key, secret_key=secret_key)

        if not success:
            return (False, minioClient)

        # check if object exists
        if not minioClient.stat_object(bucket, filename):
            return (False, "Object {} doesn't exist in bucket {}".format(filename, bucket))

        # remove it if it does
        try:
            minioClient.remove_object(bucket, filename)
            return (True, filename)
        except ResponseError as err:
            return (False, err)