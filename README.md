# st2-s3

S3-compatible storage connector for stackstorm. Based on the minio python lib to allow for a more basic interface.

I'm happy to take pull requests on this - I'm only implementing the things I need as I need them!

## Changelog

* 2019-03-01 Basic PUT/REMOVE support, tested with minio.
* 2019-03-02 Added list_buckets, make_bucket, remove_bucket, list_objects.