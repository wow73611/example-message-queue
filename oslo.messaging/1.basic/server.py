#!/usr/bin/python

from oslo_config import cfg
import oslo_messaging as messaging

NODE_NAME = 'srv1'

class Endpoints(object):
    def hello(self, ctx):
        print "[%s] Invoke hello method" % NODE_NAME
        return "Welcome to %s" % NODE_NAME

transport = messaging.get_transport(cfg.CONF)
target = messaging.Target(topic='hello', server=NODE_NAME)
server = messaging.get_rpc_server(transport, target, endpoints=[Endpoints(), ])

print "[%s] Server start" % NODE_NAME
server.start()
server.wait()
print "[%s] Server end" % NODE_NAME

