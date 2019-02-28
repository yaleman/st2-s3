#!/usr/bin/env python3


if __name__ != '__main__':
    from st2common.content import utils
    from st2common.runners.base_action import Action

class S3_upload(Action):
    def run(self, filename, cmd, s3server, access_key, secret_key, *args):
        """ uploads a file from the local disk """
        return "Hello world"