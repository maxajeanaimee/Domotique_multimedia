import msgpack
import time
import sys
import zmq
from random import choice
    

class stb():
    mode = ["mode_radio", "mode_tv", "mode_vod", "mode_rss", "mode_dvd"]
    Channel = ["channel1", "channel2", "channel3", "channel4"]
    subtitle = ["on", "off"]
    power = ["on", "off"]

    def __init__(self, mode, channel, subtitle):
        self.mode = "mode_tv"
        self.channel = "channel1"
        self.subtitle = "off"
        self.power =  "on"


    global dynamote
    global stb_rep
    global stb_pub
    global stb_sub
    global stb_pull
    global stb_push
    global port
    
    dynamote = zmq.Context()
    stb_pub = dynamote.socket(zmq.PUB)
    stb_sub = dynamote.socket(zmq.SUB)
    stb_pull = dynamote.socket(zmq.PULL)
    stb_push = dynamote.socket(zmq.PUSH)
    default_port = "5000"


   ################################ MODE SERVEUR ###############################
   #   Autoconfiguration ip_address for connect is 169.254.1.2 on the port 5000
    ip_address = str("169.254.1.2")
    # Provide port as command line argument to run server at two different ports
    if len(sys.argv)> 1:
        port = sys.argv[1]
        int(port)
    if len(sys.argv) > 2:
        port1 = sys.argv[2]
        int(port1)
    if len(sys.argv) > 3:
        port2 = sys.argv[3]
        int(port2)
        
    global stb_description
    stb_description ="Set top box is on this",ip_address,"and",default_port
    print(stb_description)
    # Bind link to dynamic discovery
    ################################### Description #######################################

    def ready_to_process(self,port):
        
        stb_rep = dynamote.socket(zmq.REP)
        stb_rep.bind("tcp://127.0.0.1:%s" %port)
        fichier_description = open ( "stb-device-api-description.json", "r")
        msg_packed = msgpack.packb(str(fichier_description))
        while True:
            msg = stb_rep.recv()
            print( "Got",msg)
            time.sleep(1)
            msg_description = str(stb_description)
            stb_rep.send(msg_packed)

    ############################### MODE CLIENT ###################################
        
        stb_req = dynamote.socket(zmq.REQ)
        print ("Attempting to connect to other process ......")
        #Connect link
        stb_req.connect("tcp://localhost:5001")
        for request in range(2):
            stb_req.send(msg_description)
            print ("Sending message")
            #  Get the reply.
            message = stb_req.recv()
            print ("Received reply ", request, "[", message, "]")

                        
    ####################### Publish_subscribe ######################################
    def subscribe_to_dvd():
        #DVD
        stb_sub.connect("tcp://*:5004")
        stb_sub.setsockopt(zmq.SUBSCRIBE, "")
        while True:
            print(stb_sub.recv())

    def subscribe_to_tv():
        # TV
        stb_sub.connect("tcp://*:5001")
        stb_sub.setsockopt(zmq.SUBSCRIBE, "")
        while True:
            print(stb_sub.recv())
            






