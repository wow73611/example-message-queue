#!/usr/bin/env python
#-*-coding:utf-8-*-

__version__ = "1.0.0"
__author__ = "robin"

from amqplib import client_0_8 as amqp

conn = amqp.Connection(
    host="127.0.0.1:5672",
    userid="guest",
    password="guest",
    virtual_host="/",
    insist=False)

chan = conn.channel()

chan.queue_declare(queue="my_queue",durable=True,exclusive=False,auto_delete=False)
chan.exchange_declare(exchange="my_exchange",type="direct",durable=True,auto_delete=False)

chan.queue_bind(queue="my_queue",exchange="my_exchange",routing_key="hello")

def recv_callback(msg):
    print 'Received: %s channel:%s' % (msg.body,str(msg.channel.channel_id))
    #chan.basic_ack(msg.delivery_tag)

chan.basic_consume(queue='my_queue',no_ack=True,callback=recv_callback,consumer_tag="my_tag")

#while True:
while chan.callbacks:
    chan.wait()

chan.basic_cancel("my_tag")
chan.close()
conn.close()
