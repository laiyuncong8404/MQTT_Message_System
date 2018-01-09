#coding:utf-8

import paho.mqtt.client as mqtt
import ssl

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("$SYS/#")

client = mqtt.Client(client_id="a:3c91579ff957", clean_session=True)
client.on_connect = on_connect
client.username_pw_set("15922614173", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.ImFhYSI.K0oDWBoeLhnYMe5QrA5wLaVynQKnfIeX3Q1jA5tR_lU")	#Connect with Username / Password
client.tls_set("/Users/xiaoxue/Documents/安全部证书/cacert.pem")#,
               #"/Users/antares/Tools/rabbitmq/tls/client_certificate.pem",
               #"/Users/antares/Tools/rabbitmq/tls/client_key.pem")
# disables peer verification
client.tls_insecure_set(True)
client.connect("mqtt.mymlsoft.com", 8883, 60)

client.loop_forever()