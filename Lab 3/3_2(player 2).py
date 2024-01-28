#MQTT Version player 2
import random
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    client.subscribe("p1_logi", 1) #add subscription for each player added, format: p#_s where # is the player number and s is the sever name

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected Disconnect")
    else:
        print("Expected Disconnect")

p1_O = " "
def on_message(client, userdata, message):
    global p1_O
    if(message.topic == "p1_logi"):
        p1_O = message.payload.decode()

if __name__ == "__main__":
    p1_r = 0
    r, p, s= "Rock","Paper","Scissors"
    Scores = [0,0] #Scores[0] = player 1's score and so on
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message


    client.connect_async("mqtt.eclipseprojects.io")

    client.loop_start()

    while(True):
        print("Please enter Rock, Paper, or Scissors: ", end="")
        User_O = input()

        if(User_O != r and User_O != p and User_O != s):
            print("Invaild Input!")
            continue
        
        client.publish("p2_logi", User_O,1) 

        while(p1_O == " "):
            if(p1_r == 0):
                print("Waiting for the input from player 1")
                p1_r = p1_r + 1
            else:
                continue
        
        print("Player1: " + p1_O)
        print("Player2: " + User_O)
        if(p1_O == User_O):
            print("Result: Tie")
        else:
            if((User_O == r and p1_O == s) or (User_O == p and p1_O == r) or (User_O == s and p1_O == p)):
                Scores[0] = Scores[0] + 1
                print("Result: Player 2 Win")
            else:
                Scores[1] = Scores[1] + 1
                print("Result: Player 1 Win")

        print("===============================================================")
        print("Player1's Score: " + str(Scores[0]))
        print("Player2's Score: " + str(Scores[1]))
        print("===============================================================")
        p1_O = " "
        p1_r = 0