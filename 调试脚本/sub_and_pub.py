#coding:utf-8
from connect import *

# msg_total = 10


client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
connect_broker(client)

client.loop_start()

client.subscribe("encyclopedia/#", qos=1)
client.subscribe("house/#", qos=1)
wait_for(client,2)
# client.loop_forever()

msg_count = 1
while msg_count <= msg_total:
	temperature_payload = str(msg_count) + " Degree"

	if msg_count % 2 == 0:
		house_payload = "OFF"
	else:
		house_payload = "ON"

	msg_info1 = client.publish(topic="house/main-light", payload=house_payload, qos=1)
	msg_info2 = client.publish("encyclopedia/temperature", temperature_payload, qos=1, retain=False)
	time.sleep(2)
	if msg_info1.is_published() == True & msg_info2.is_published() == True:
		print("Topic 'house'&'temperature' all published done!")
	else:
		print("Topic 'house'&'temperature' are not yet published.")
		msg_info.wait_for_publish()	# This call will block until the message is published.
	msg_count += 1

# client.unsubscribe("encyclopedia/#")
client.loop_stop()

