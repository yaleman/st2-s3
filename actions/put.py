#!/usr/bin/env python

from tempfile import NamedTemporaryFile
import os.path

from io import StringIO

from client import minio_client
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)

if __name__ != '__main__':
    from st2common.content import utils
    from st2common.runners.base_action import Action

class S3_put(Action):
    def run(self, endpoint_secure=True, endpoint=None, access_key=None, secret_key=None, filename=None, filedata=None, filesource=None, bucket=None, location=None):
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
        #upload the file
        try:
            if filedata:
                self.logger.debug("Writing input content to '{}/{}'".format(bucket, filename))
                with NamedTemporaryFile() as fh:
                    fh.write(filedata)
                    fh.seek(0)
                    if minioClient.put_object(bucket, filename, fh, len(filedata)):
                        return (True, "Wrote '{}/{}'".format(bucket, filename))
                    else:
                        return (False, "Failed to write filedata to '{}/{}'".format(bucket, filename))
            else:
                if os.path.exists(filesource):
                    self.logger.debug("Found file: '{}'".format(filesource))
                    if minioClient.fput_object(bucket, filename, filesource):
                        return (True, "Write file from '{} to '{}/{}'".format(filesource, bucket, filename))
                    else:
                        return (False, "Failed to write file from '{}' to '{}/{}'".format(filesource, bucket, filename))
                else:
                    return (False, "Couldn't find file '{}'".format(filesource))
        except ResponseError as err:
            return (False, err)
        return (False, "Failed for some reason")