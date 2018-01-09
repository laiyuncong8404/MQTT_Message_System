#coding:utf-8
import time
import logging
import paho.mqtt.client as mqtt
import json
import struct
import ssl

global broker_address
broker_address = "mqtt.mymlsoft.com"
broker_port = 8883

device_sn = "G291072808CD201712260001" #XMPP Device of waterHeater
app_sn = "bd4ec3be13214f20" #13688406231
app_client_id = "a:" + app_sn
app_msg_topic = "d/" + device_sn + "/i"
json_dict = "080100040001030E142D000400000000"
msg_payload = struct.pack('B',len(app_sn)) + app_sn.encode('ascii') + json_dict
#序列化成str方法1
# msg_payload = struct.pack('B',len(app_sn)) + app_sn.encode('ascii') + bytes(json.dumps(json_dict))
#序列化成str方法2
# msg_payload = str(len(app_sn) + app_sn.encode('ascii') + bytes(json.dumps(json_dict))
print "The getStatus string is: " ,msg_payload
# msg_getStatus = json.dumps({"msgtype":"instantstatus","devtype":"1281"}).encode('ascii')
# msg_on = json.dumps({"msgtype":"order", "ordertype":0, "ordercode":1, "ordervalue":"1","type":"1281"}).encode('ascii')
# msg_off = json.dumps({"msgtype":"order", "ordertype":0, "ordercode":1, "ordervalue":"0","type":"1281"}).encode('ascii')

def on_connect(client, userdata, flags, rc):
	print("Connect received of code %d." % (rc))
	if rc == 0:
		print("Client connected success")
	else:
		print("Client connected FAIL")

def on_disconnect(client, userdata, rc):
	print("Disconnect received of code %d." % (rc))
	if rc == 0:
		print("Client disconnect success")
	else:
		print("Client disconnect FAIL")
 
def on_subscribe(client, userdata, mid, granted_qos):
	print("Subscribed topic: " + str(mid) + " " + str(granted_qos))

def on_publish(client, userdata, mid):
	print("Publish to topic: " + str(mid))

def on_message(client, userdata, msg):
	print("message topic=", msg.topic)
	print("message received " , str(msg.payload))
	print("message qos=", msg.qos)
	print("message retain flag=", msg.retain)

def on_log(client, userdata, MQTT_LOG_DEBUG, buf):
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

	client.username_pw_set(app_sn, "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.ImFhYSI.K0oDWBoeLhnYMe5QrA5wLaVynQKnfIeX3Q1jA5tR_lU")	#Connect with Username / Password
	client.tls_set("/Users/xiaoxue/Documents/安全部证书/emqtt_androidbks/root.crt", certfile=None, keyfile=None, cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)
#disables peer verification by set 'True'
	# client.tls_insecure_set(True)
#connect
	client.enable_logger(logger = None)
	client.connect(host=broker_address, port=broker_port, keepalive=60, bind_address="")

if __name__ == "__main__":
	client = mqtt.Client(client_id=app_client_id, clean_session=True, userdata=None, protocol=mqtt.MQTTv31)	
	connect_broker(client)
	wait_for(client, 3)
	client.loop_start()	
	msg_info = client.publish(topic=app_msg_topic, payload=msg_payload, qos=1, retain=False)
 	time.sleep(5)
	if msg_info.is_published() == False:
		print("Query topic from APP is not yet published.")
		msg_info.wait_for_publish()	# This call will block until the message is published.
	else:
		print("Query topic from APP published done!")

	# client.publish(topic=app_msg_topic, payload=msg_getStatus, qos=1, retain=False)
	# time.sleep (5)
	# client.publish(topic=app_msg_topic, payload=msg_off, qos=1, retain=False)
	# time.sleep (5)
	# client.publish(topic=app_msg_topic, payload=msg_on, qos=1, retain=False)
	# client.loop_stop()
	# client.disconnect()
	# client.loop_forever(retry_first_connection=True)
	while True:
		time.sleep(1)