#!/usr/bin/env python
#-*-coding:utf-8-*-

__version__ = "1.0.0"
__author__ = "robin"

import sys
from amqplib import client_0_8 as amqp

conn = amqp.Connection(
    host="127.0.0.1:5672",
    userid="guest",
    password="guest",
    virtual_host="/",
    insist=False)

ch = conn.channel()

msg = amqp.Message(sys.argv[1])
msg.properties["content_type"] = "text/plain"
msg.properties["delivery_mode"] = 2
ch.basic_publish(msg=msg,exchange="my_exchange",routing_key="hello")

ch.close()
conn.close()
