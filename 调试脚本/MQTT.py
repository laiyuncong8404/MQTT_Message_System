#coding:utf-8
import time
import paho.mqtt.client as mqtt

broker_address = "10.3.93.241"

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
	print("message received " , str(msg.payload))
	print("message topic=", msg.topic)
	print("message qos=", msg.qos)
	print("message retain flag=", msg.retain)

def on_log(client, userdata, level, buf):
	print("logging: ", buf)

def wait_for(client, msgType, period=5):
	if msgType=="SUBACK":
		if client.on_subscribe:
			while not client.suback_flag:
				logging.info("waiting suback")
				client.loop()  #check for messages
				time.sleep(period)

def sample_1():
	print("Creating new instance……")
	client = mqtt.Client() #create new instance
	client.on_message = on_message #attach function to callback
	client.on_log = on_log
	client.on_connect = on_connect
	print("Connecting to broker……")
	# client.username_pw_set("admin", "public")	#Connect with Username / Password
	client.connect(broker_address, port=1883) #connect to broker
	client.loop_start() #start the loop
	print("Subscribing topic: " + "house/bulbs/bulb1")
	client.subscribe("house/bulbs/bulb1")
	print("Publishing message to topic: " + "house/bulbs/bulb1")
	client.publish("house/bulbs/bulb1","OFF")
	time.sleep(10) # wait
	client.loop_stop() #stop the loop

if __name__ == "__main__":
	client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
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
#subscribe
	client.loop_start()
	client.subscribe("encyclopedia/#", qos=1) 
#publish
 	msg_info = client.publish("encyclopedia/temperature", "25degree", qos=1, retain=False)
 	time.sleep(10)
	if msg_info.is_published() == False:
		print("Topic is not yet published.")
	else:
		print("Topic published done!")
	msg_info.wait_for_publish()	# This call will block until the message is published.
#Unsubscribe
	client.subscribe("$SYS/broker/version", 0)

	client.unsubscribe("encyclopedia/#")
#disconnect
	client.loop_stop()
	# client.loop_forever()
	# client.disconnect()

