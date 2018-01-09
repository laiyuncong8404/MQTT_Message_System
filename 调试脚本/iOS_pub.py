#coding:utf-8
import re, string, random
from connect import *

# msg_total = 10

def id_generator(size=4, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    #[random.choice(chars) for _ in range(size)]为列表解析
    #(random.choice(chars) for _ in range(size))为生成器，其对内存更友好
    list = []
    for i in range(msg_total):
        a = ''.join(random.choice(chars) for _ in range(size))
        list.append(a)
    # print list
    return list

client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
connect_broker(client)

client.loop_start()
msg_count = 1
while msg_count <= msg_total:
	topic = "mqtt/iOS/pub/"+id_generator()[msg_count-1]+"/"
	payload = str(msg_count) + " Degree"
	msg_info = client.publish(topic, payload, qos=1, retain=False)
	time.sleep(2)
	if msg_info.is_published() == True:
		print("Topic 'mqtt/iOS/pub/' all published done!")
	else:
		print("Topic 'Topic 'mqtt/iOS/pub/' are not yet published.")
		msg_info.wait_for_publish()
	msg_count += 1
client.loop_stop()