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
logger = log.getLogger(__name__)


class Client(object):
    def __init__(self, transport):
        self.transport = transport
        self.host = transport.conf.host
        self.target = messaging.Target(topic='hello',server=self.host)
        #self.target = messaging.Target(topic='hello')
        self.client = messaging.RPCClient(self.transport,self.target)

    def send(self, ctxt={}, args=None):
        logger.info("[client] Send - ctxt=%s args=%s",ctxt,args)
        cctxt = self.client.prepare(timeout=60)
        # try: except:
        #return cctxt.call(ctxt,'hello',args=args)
        return cctxt.cast(ctxt,'hello',args=args)

transport = messaging.get_transport(CONF)
logger.info("[client] Transport created")

client = Client(transport)
logger.info("[client] Client created")

#while True:
now_time = time.strftime("%Y-%m-%d %H:%M:%S")
payload = {'name': 'robin', 'time': now_time}
result = client.send({},payload)
logger.info("[client] Receive - result=%s",result)
time.sleep(5)

