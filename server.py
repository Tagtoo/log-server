#!/usr/bin/python
import time
import gevent
import gevent.monkey
import gevent.server
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()
import logging
import logging.config
import yaml
import sys
import os

logger = logging.getLogger("system")

def application(env, start_response):
    path = env['PATH_INFO']
    qs = env['QUERY_STRING']
    logger.info(path + "?" + qs)

    start_response('204 No Content', [])
    return []

class LogServer(gevent.server.DatagramServer):
    def handle(self, data, address):
        logger.info(data)


def upload(filename, bucket):
    for i in os.listdir('.'):
         if filename +'.' in i and '.gz' not in i:
            ipath = i
            os.system('gzip %s' % ipath)
            os.system('gsutil cp %s.gz gs://%s' % (ipath, bucket))

    time.sleep(5*60)

def start(bucket, type="TCP", port=8080, filename="request.log", when="H"):
    config = yaml.load(open('conf.yaml', 'r').read().format(**{
        "filename": filename,
        "when": when
    }))
    logging.config.dictConfig(config)

    print('Serving %s on %s...' % (type, port ))
    gevent.spawn(upload, filename, bucket)

    if type == "TCP":
        WSGIServer(('', port), application).serve_forever()
    else:
        LogServer(":%s" % port).serve_forever()


if __name__ == '__main__':
#    import clime; clime.start()
    start('tagtoo_rtb_log', type="UDP")

