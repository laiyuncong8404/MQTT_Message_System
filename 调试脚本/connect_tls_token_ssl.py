#coding:utf-8
import time
import logging
import paho.mqtt.client as mqtt
import ssl

global broker_address
broker_address = "mqtt.mymlsoft.com"
broker_port = 8883
global msg_total
msg_total = 10

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
#connect with Username / Password
	client.username_pw_set("3c91579ff957", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.ImFhYSI.K0oDWBoeLhnYMe5QrA5wLaVynQKnfIeX3Q1jA5tR_lU")
	# client.tls_set("/Users/xiaoxue/Documents/安全部证书/cacert.pem", certfile=None, keyfile=None, cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)
	client.tls_set("/Users/xiaoxue/Documents/安全部证书/emqtt_androidbks/root.crt", certfile=None, keyfile=None, cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)
#disables peer verification by set 'True'
	# client.tls_insecure_set(True)
	client.user_data_set("")
	client.will_set("Byebye/#", payload=None, qos=0, retain=False)	#Connect with LastWillSet
#connect
	client.connect(host=broker_address, port=broker_port, keepalive=60, bind_address="")


if __name__ == "__main__":
	client = mqtt.Client(client_id="a:3c91579ff957", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
	connect_broker(client)
#subscribe
	client.loop_start()	
	client.subscribe("$SYS/broker/version", qos=0)
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

#unsubscribe
	client.unsubscribe("encyclopedia/#")
#disconnect
	client.loop_stop()
	client.disconnect()

