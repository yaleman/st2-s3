#!/usr/bin/env python

if __name__ != '__main__':
    from st2common.content import utils
    from st2common.runners.base_action import Action

class S3_put(Action):
    def run(self, **args):
        """ uploads a file from the local disk """
        return "Hello world"