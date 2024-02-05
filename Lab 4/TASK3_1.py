import paho.mqtt.client as mqtt
import numpy as np

def on_connect(client, userdata, flags, rc):
    client.subscribe("lol123", 1) 

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected Disconnect")
    else:
        print("Expected Disconnect")

def on_message(client, userdata, message):
    print("======================================================================")
    print("Received message: " + str(message.payload) + " on topic " +
    message.topic)



client = mqtt.Client()

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message


client.connect_async("mqtt.eclipseprojects.io")

client.loop_start()


print("Connection will be disconnect upon typing END to the message")

while True:
    msg = input("Enter the message you wish to send: \n")
    client.publish("lol123", msg,1) 
    if(msg == "END"):
        break
    


client.loop_stop()
client.disconnect()