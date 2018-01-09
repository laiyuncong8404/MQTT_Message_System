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
	temperature_topic = "encyclopedia/temperature/"+id_generator()[msg_count-1]+"/"
	temperature_payload = str(msg_count) + " Degree"

	if msg_count % 2 == 0:
		house_payload = "OFF"
	else:
		house_payload = "ON"

	msg_info1 = client.publish(topic="house/main-light", payload=house_payload, qos=1)
	msg_info2 = client.publish(temperature_topic, temperature_payload, qos=1, retain=False)
	time.sleep(2)
	if (msg_info1.is_published() == True) and (msg_info2.is_published() == True):
		print("Topic 'house'&'temperature' all published done!")
	else:
		print("Topic 'house'&'temperature' are not yet published.")
		msg_info1.wait_for_publish()
		msg_info2.wait_for_publish() 	# This call will block until the message is published.
	msg_count += 1

# client.unsubscribe("encyclopedia/#")
client.loop_stop()