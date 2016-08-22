#!/usr/bin/python

from oslo_config import cfg
import oslo_messaging as messaging

NODE_NAME = 'srv1'

transport = messaging.get_transport(cfg.CONF)
#target = messaging.Target(topic='hello')
target = messaging.Target(topic='hello',server=NODE_NAME)
client = messaging.RPCClient(transport, target)

try:
    print client.call({},'hello')
except:
    print "Error: Remote method is not found"

