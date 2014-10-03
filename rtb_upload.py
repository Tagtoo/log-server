#!/usr/bin/env python

from protobuf_json import *
from realtime_bidding_pb2 import *
import re
import json
import gzip
import os
import time
from  gcloud import storage

pattern = re.compile(r'([\d]{4}\-[\d]{2}\-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2},[\d]{3}) REQ:(.*)RESP:(.*)', re.DOTALL)

def buf_read(io, buffer_size=10000):
    buf = io.read(buffer_size)
    while True:
        if '\n#!#' in buf:
            i, buf = buf.split('\n#!#', 1)
            yield i
        else:
            chunk = io.read(buffer_size)
            if not chunk:
                yield buf
                break

            buf += chunk


def convert(filename, ofile):
    io = open(filename)
    request = BidRequest()
    response = BidResponse()

    ofile = gzip.GzipFile(ofile, 'w')
    for line in buf_read(io):
        try:
            m = pattern.findall(line)
            if m:
                time, req, resp = m[0]
                request.ParseFromString(req)
                response.ParseFromString(resp)
                req = pb2json(request)
                resp = pb2json(response)

                # add some reference property
                req['time'] = time
                req['_type'] = 'BidRequest'
                resp['time'] = time
                resp['request_id']  = req['id']
                resp['_type'] = 'BidResponse'

                ofile.write(json.dumps(req) + '\n')
                ofile.write(json.dumps(resp) + '\n')
        except:
            print line

def upload(filename, bucket):
    client = storage.get_bucket(
        bucket,
        "tagtooadex2",
        "1065106153444-mdj042q86ciof489e71i49joe6an21k6@developer.gserviceaccount.com",
        "tagtooadex2-9e2928ac0acf.p12"
    )
    client.upload_file(filename, filename)
    os.remove(filename)

def start(filename, bucket):
    for i in os.listdir('.'):
        if '%s.'%filename in i and '.gz' not in i:
            ipath = './%s' % i
            opath = './%s.gz' % i.replace('request.log.', 'request.json.')
            convert(ipath, opath)
            os.remove(ipath)
            upload(opath, bucket)

import re
if __name__ == "__main__":
    import clime; clime.start(default="start")
