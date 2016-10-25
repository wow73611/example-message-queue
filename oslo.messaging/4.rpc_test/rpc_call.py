#!/usr/bin/env python
#-*-coding:utf-8-*-

__version__ = "1.0.0"
__author__ = "robin"

import multiprocessing
import time
import sys
import logging
import signal
import traceback
from oslo_config import cfg
import oslo_messaging as messaging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

NODE_NAME = 'srv1'
RPC_TOPIC = 'a-test'

CONF = cfg.CONF
CONF(sys.argv[1:])

def handler(signum, frame):
    print 'signal', signum
    return

def client_worker():
    print '[Client] Worker start ...'
    def client_handler(signum, frame):
        print '[Client] Client handler %s' % signum
        raise Exception()

    signal.signal(signal.SIGTERM, client_handler)
    signal.signal(signal.SIGINT, client_handler)
    client_process()
    print '[Client] Worker end ...'

def client_process():
    transport = messaging.get_transport(cfg.CONF)
    target = messaging.Target(topic=RPC_TOPIC,server=NODE_NAME)
    client = messaging.RPCClient(transport, target)
    try:
        for i in xrange(100):
            print '[Client] Request - %s' % i
            result = client.call({'i':i},'worker',)
            print '[Client] Respond - %s\n' % result
            time.sleep(5)
    except Exception as e:
        print '[Client] %s' % traceback.format_exc()

class Endpoints(object):
    def worker(self, ctx):
        print "[Server] Worker - [%s] %s" % (NODE_NAME,ctx)
        return "Welcome to [%s] - %s" % (NODE_NAME,ctx)

def server_worker():
    print '[Server] Worker start ...'
    def server_handler(signum, frame):
        print '[Server] Server handler %s' % signum
        raise Exception()

    signal.signal(signal.SIGTERM, server_handler)
    signal.signal(signal.SIGINT, server_handler)
    server_process()
    print '[Server] Worker end ...'

def server_process():
    transport = messaging.get_transport(cfg.CONF)
    target = messaging.Target(topic=RPC_TOPIC, server=NODE_NAME)
    server = messaging.get_rpc_server(transport, target, endpoints=[Endpoints(), ])

    server.start()
    print '[Server] %s wait ...' % NODE_NAME
    server.wait()
    print '[Server] Worker end ...'

def main():
    print '[Main] start ...'
    proc_list = []
    for proc in [server_worker,client_worker]:
        proc_list.append(multiprocessing.Process(target=proc))
    print '[Process] start ...'
    r = [proc.start() for proc in proc_list]

    try:
        print '[Process] join ...'
        r = [proc.join() for proc in proc_list]
    except KeyboardInterrupt:
        print '[Process] KeyboardInterrupt ...'
        r = [proc.terminate() for proc in proc_list]
        r = [proc.join() for proc in proc_list]
    except Exception as e:
        print '[Process] %s' % traceback.format_exc()
    print '[Main] end ...'

if __name__ == '__main__':
    main()

"""
python rpc_call.py --config-file config.conf
"""
