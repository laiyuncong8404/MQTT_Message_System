#coding:utf-8
from connect import *

client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
connect_broker(client)

client.subscribe("mqtt/iOS/#", qos=1)
wait_for(client, 5)
client.loop_forever()