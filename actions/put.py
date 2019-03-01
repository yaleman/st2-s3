#!/usr/bin/env python

from client import minio_client


if __name__ != '__main__':
    from st2common.content import utils
    from st2common.runners.base_action import Action

class S3_put(Action):
    def run(self, endpoint_secure=True, endpoint=None, access_key=None, secret_key=None, filename=None, filesource=None, bucket=None, location=None):
        """ uploads a file from the local disk """

        # check supplied config and set global config if available

        # Initialize minioClient with an endpoint and access/secret keys.
        success, minioClient = minio_client(self, endpoint=endpoint, endpoint_secure=endpoint_secure, access_key=access_key, secret_key=secret_key)

        if not success:
            return (False, minioClient)
        
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