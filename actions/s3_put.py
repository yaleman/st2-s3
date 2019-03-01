#!/usr/bin/env python

from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)


if __name__ != '__main__':
    from st2common.content import utils
    from st2common.runners.base_action import Action

class S3_put(Action):
    def run(self, endpoint_secure=True, endpoint=None, access_key=None, secret_key=None, filename=None, filesource=None, bucket=None, location=None):
        """ uploads a file from the local disk """

        # check supplied config and set global config if available

        # if endpoint is set by global, you can't change enpdoint_secure in the call
        if not endpoint and self.config.get('endpoint', False):
            endpoint = self.config['endpoint']
            endpoint_secure = self.config['endpoint_secure']
        if not access_key and self.config.get('access_key', False):
            access_key = self.config['access_key']
        if not secret_key and self.config.get('secret_key', False):
            secret_key = self.config['secret_key']
        
        # Initialize minioClient with an endpoint and access/secret keys.
        minioClient = Minio(endpoint,
                            access_key=access_key,
                            secret_key=secret_key,
                            secure=endpoint_secure)

        # Make a bucket with the make_bucket API call.
        try:
            if location:
                minioClient.make_bucket(bucket, location=location)
            else:
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
                return (True, "Successfully uploaded {}".format(filename))
            except ResponseError as err:
                return (False, err)