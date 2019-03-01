#!/usr/bin/env python

from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)


if __name__ != '__main__':
    from st2common.content import utils
    from st2common.runners.base_action import Action

class S3_put(Action):
    def run(self, secure=True, endpoint=None, access_key=None, secret_key=None, filename=None, filesource=None, bucket=None):
        """ uploads a file from the local disk """
        # Initialize minioClient with an endpoint and access/secret keys.
        minioClient = Minio(endpoint,
                            access_key=access_key,
                            secret_key=secret_key,
                            secure=secure)

        # Make a bucket with the make_bucket API call.
        try:
            minioClient.make_bucket(bucket)
        except BucketAlreadyOwnedByYou as err:
            pass
        except BucketAlreadyExists as err:
            pass
        except ResponseError as err:
            raise
        else:
            try:
                minioClient.fput_object(bucket, filename, filesource)
                return True
            except ResponseError as err:
                print(err)