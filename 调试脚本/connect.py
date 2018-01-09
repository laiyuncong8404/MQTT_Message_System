#coding:utf-8
import time
import logging
import paho.mqtt.client as mqtt

global broker_address
broker_address = "10.3.93.241"
global msg_total
msg_total = 20

def on_connect(client, userdata, flags, rc):
	print("Connect received of code %d." % (rc))

def on_disconnect(client, userdata, rc):
	print("Disconnect received of code %d." % (rc))
	print("Client disconnected ok")
 
def on_subscribe(client, userdata, mid, granted_qos):
	print("Subscribed topic: " + str(mid) + " " + str(granted_qos))

def on_publish(client, userdata, mid):
	print("Publish to topic: " + str(mid))

def on_message(client, userdata, msg):
	print("message topic=", msg.topic)
	print("message received " , str(msg.payload))
	print("message qos=", msg.qos)
	print("message retain flag=", msg.retain)

def on_log(client, userdata, level, buf):
	print("logging: ", buf)

def wait_for(client, msgType, period=5):
	if msgType=="SUBACK":
		if client.on_subscribe:
			while not client.suback_flag:
				logging.info("waiting suback……")
				client.loop()  #check for messages
				time.sleep(period)

def connect_broker(client):
	client.on_log = on_log
	client.on_disconnect = on_disconnect
	client.on_connect = on_connect
	client.on_message = on_message
	client.on_subscribe = on_subscribe
	client.on_publish = on_publish

	client.username_pw_set("admin", "public")	#Connect with Username / Password
	client.will_set("Byebye/#", payload=None, qos=0, retain=False)	#Connect with LastWillSet
#connect
	client.connect(host=broker_address, port=1883, keepalive=60, bind_address="")


if __name__ == "__main__":
	client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
	connect_broker(client)
#subscribe
	client.loop_start()	
	client.subscribe("$SYS/broker/version", 0)
	client.subscribe("encyclopedia/#", qos=1) 
#publish
	msg_count = 1
	while msg_count <= msg_total:
		temperature_payload = str(msg_count) + " Degree"

 		msg_info = client.publish(topic="encyclopedia/temperature", payload=temperature_payload, qos=1, retain=False)
 		time.sleep(5)
		if msg_info.is_published() == False:
			print("Topic is not yet published.")
			msg_info.wait_for_publish()	# This call will block until the message is published.
		else:
			print("Topic published done!")
		msg_count += 1

#Unsubscribe
	client.unsubscribe("encyclopedia/#")
#disconnect
	client.loop_stop()
	client.disconnect()

