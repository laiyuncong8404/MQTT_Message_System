#coding:utf-8
from connect import *

client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
connect_broker(client)

client.subscribe("$SYS/broker/version", qos=0)
client.subscribe("encyclopedia/#", qos=1)
client.subscribe("house/#", qos=1)
wait_for(client, 5)
# client.unsubscribe("encyclopedia/#")
client.loop_forever()