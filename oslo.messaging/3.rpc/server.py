#!/usr/bin/python

import time
import sys
import logging

from oslo_log import log
from oslo_config import cfg
import oslo_messaging as messaging

opts = [
    cfg.StrOpt('host', default='srv1')
]
CONF = cfg.CONF
CONF.register_opts(opts)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
#log.setup(CONF,'rpc')
logger = log.getLogger(__name__)


class Server(object):
    def __init__(self, transport):
        self.transport = transport
        self.host = transport.conf.host
        self.target = messaging.Target(topic='hello',server=self.host)
        self.server = messaging.get_rpc_server(self.transport,self.target,[self])

    def start(self):
        logger.info("[%s] Server started",self.host)
        self.server.start()

    def wait(self):
        logger.info("[%s] Server waited",self.host)
        self.server.wait()

    def hello(self, ctx, args=[]):
        logger.info("[%s] Invoke hello - args=%s",self.host,args)
        time.sleep(3)
        now_time = time.strftime("%Y-%m-%d %H:%M:%S")
        result = "Welcome to %s, now is %s" % (self.host,now_time)
        logger.info("[%s] Respond hello - result=%s",self.host,result)
        return result


if __name__ == '__main__':
    transport = messaging.get_transport(CONF)
    logger.info("[%s] Transport created",CONF.host)
    server = Server(transport)
    logger.info("[%s] Server created",CONF.host)
    server.start()
    server.wait()


