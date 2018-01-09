#coding:utf-8
import time
import logging
import paho.mqtt.client as mqtt
import json
import ssl

global msg_total
msg_total = 1
global broker_address
broker_address = "mqtt.mymlsoft.com"
broker_port = 8883

device_sn = "G291070341CD201712201624" #XMPP Device of waterHeater
device_client_id = "d:" + device_sn
device_msg_topic = "x/" + device_sn + "/m"
device_status_topic = "x/" + device_sn + "/s"

# app_sn = "f4d6b7a090a94b79" #18908030702
app_sn = "bd4ec3be13214f20" #13688406231

app_client_id = "a:" + app_sn
app_msg_topic = "xmpp/" + "d/" + device_sn + "/i"

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
	print("message received ", str(msg.payload))
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

if __name__ == "__main__":
#Connect with Username / Password
	client_app = mqtt.Client(client_id=app_client_id, clean_session=True, userdata=None, protocol=mqtt.MQTTv31)	
	client_app.username_pw_set(app_sn, "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ0YW8xLmppYW5nIiwidXNlciI6ImU0OGIzMzdkNjU3YTQ0MTcifQ.B9X1lyIC--zZ-OD_Scjd-eC9bTlCe8Owhs0dfdRT4_0")
	client_app.tls_set("/Users/xiaoxue/Documents/安全部证书/emqtt_androidbks/root.crt", certfile=None, keyfile=None, cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)
	client_app.tls_insecure_set(True)
	client_app.connect(host=broker_address, port=broker_port, keepalive=60, bind_address="")
	
	client_device = mqtt.Client(client_id=device_client_id, clean_session=True, userdata=None, protocol=mqtt.MQTTv31)	
	client_device.username_pw_set(device_sn, "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ0YW8xLmppYW5nIiwidXNlciI6IkQzQTYwMDQ3MDdMTVRFMTcxMTIxMDAwMSJ9.oO5JM8Zvq3upk6DGDElPdecs2wRUiXT9uckI4aatyq0")
	client_device.tls_set("/Users/xiaoxue/Documents/安全部证书/emqtt_androidbks/root.crt", certfile=None, keyfile=None, cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)
	client_device.tls_insecure_set(True)
	client_device.connect(host=broker_address, port=broker_port, keepalive=60, bind_address="")
	
	connect_broker(client_app)
	connect_broker(client_device)
#subscribe
	client_app.loop_start()	
	client_device.loop_start()	
	# client_device.subscribe("$share/bridge/xmpp/#", qos=1)
#publish
	msg_count = 1
	while msg_count <= msg_total:
		# json_dict = {"getTemperature": {"action": "INVOKE_SDK_FUNCTION", "functions": [{"ParameterList": [], "name": "getSyncAcStatus"}]}}
		# app_msg_payload = '11' + app_sn + json.dumps(json_dict) #序列化成str
		app_msg_payload = "080100040001030E142D000400000000"
		device_msg_payload = str(msg_count) + " degree, msg from XMPP Device"
		if msg_count % 2 == 0:
			device_status_payload = "0, Offline status from XMPP Device"
		else:
			device_status_payload = "1, Online status from XMPP Device"
 		
 		app_msg_info = client_app.publish(topic=app_msg_topic, payload=app_msg_payload, qos=1, retain=False)
		device_msg_info = client_device.publish(topic=device_msg_topic, payload=device_msg_payload, qos=1, retain=False)
 		device_status_info = client_device.publish(topic=device_status_topic, payload=device_status_payload, qos=1, retain=False)
 		
 		time.sleep(5)
		if app_msg_info.is_published() == False or device_msg_info.is_published() == False or device_status_info.is_published() == False:
			print("Topic is not yet published.")
			app_msg_info.wait_for_publish()	# This call will block until the message is published.
		else:
			print("Topic published done!")
		msg_count += 1
		
#unsubscribe
	# client_device.unsubscribe("$SYS/broker/version")
#disconnect
	client_device.loop_stop()
	client_device.disconnect()
	client_app.loop_stop()
	client_app.disconnect()
	