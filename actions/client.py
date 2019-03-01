#!/usr/bin/env python

from minio import Minio

def minio_client(action, endpoint=None, endpoint_secure=True, access_key=None, secret_key=None):
    """ instantiates a new client connection, does a bunch of stackstorm-specific checks first """
    if not endpoint:
        if action.config.get('endpoint', False):
            endpoint = action.config['endpoint']
            endpoint_secure = action.config['endpoint_secure']
        else:
            return (False, "Endpoint not specified")
    if not access_key:
        if action.config.get('access_key', False):
            access_key = action.config['access_key']
        else:
            return (False, "No access key specified")
    if not secret_key:
        if action.config.get('secret_key', False):
            secret_key = action.config['secret_key']
        else:
            return (False, "No secret key specified")
    
    return (True, Minio(endpoint_secure, endpoint, access_key, secret_key))