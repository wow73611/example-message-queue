#!/usr/bin/python

import threading
import time

from oslo_config import cfg
import oslo_messaging as messaging

opts = [
    cfg.StrOpt('host', default='srv1')
]
CONF = cfg.CONF
CONF.register_opts(opts)

class Server(object):
    def __init__(self, transport):
        self.transport = transport
        self.host = transport.conf.host
        self.target = messaging.Target(topic='hello',server=self.host)
        self.server = messaging.get_rpc_server(self.transport,self.target,[self])

    def start(self):
        print "[%s] Server start" % self.host
        self.server.start()

    def wait(self):
        print "[%s] Server wait" % self.host
        self.server.wait()

    def hello(self, ctx, args=[]):
        print "[%s] Invoke hello method args=%s" % (self.host,args)
        return "Welcome to %s" % self.host

class Client(object):
    def __init__(self, transport):
        self.transport = transport
        self.host = transport.conf.host
        self.target = messaging.Target(topic='hello',server=self.host)
        self.client = messaging.RPCClient(self.transport,self.target)

    def send(self, ctxt, args):
        print "[client] Send ctxt: %s args: %s" % (ctxt,args)
        cctxt = self.client.prepare()
        # try: except:
        return cctxt.call(ctxt,'hello',args=args)


transport = messaging.get_transport(CONF)
server = Server(transport)
#server.start()
#server.wait()
thread = threading.Thread(target=server.start)
thread.daemon = True
print "[%s] Thread starting" % transport.conf.host
thread.start()
print "[%s] Thread started" % transport.conf.host

client = Client(transport)
while True:
    print "[client] Receive: %s" % client.send({},{'name':'robin'})
    time.sleep(5)
    while thread.isAlive():
        thread.join(.05)

