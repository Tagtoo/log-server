#!/usr/bin/env python

import os
import time
from gcloud import storage

def upload(filename, bucket):
    client = storage.get_bucket(
        bucket,
        "tagtooadex2",
        "1065106153444-mdj042q86ciof489e71i49joe6an21k6@developer.gserviceaccount.com",
        "tagtooadex2-9e2928ac0acf.p12"
    )

    for i in os.listdir('.'):
        if '%s.' % filename in i and '.gz' not in i:
            print 'start upload', i, bucket
            ipath = './%s' % i
            os.system('gzip %s' % ipath)
            client.upload_file(ipath, ipath)
            os.remove(ipath)

if __name__ == "__main__":
    import clime; clime.start()
