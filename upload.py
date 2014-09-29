#!/usr/bin/env python

import os
import time

def upload(filename, bucket):
    for i in os.listdir('.'):
        if '%s.' % filename in i and '.gz' not in i:
            print 'start upload', i, bucket
            ipath = './%s' % i
            os.system('gzip %s' % ipath)
            os.system('gsutil mv %s.gz gs://%s' % (ipath, bucket))

if __name__ == "__main__":
    import clime; clime.start()
