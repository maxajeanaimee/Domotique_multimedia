import msgpack
import sys
import zmq
import time
import socket
from random import choice


class tv():
    
    channnel =  ["channel1","channel2", "channel3","channel4"]
    power = ["on","off"]
    state_on_dvd = ["false","true"]


    def __init__(self,channel):
        self.channel = "channel1"
        power = "on"
        self.state_on_dvd = "false"

    global dynamote
    global tv_req
    global tv_push
    global tv_sub
    global tv_pub
    global tv_rep
        
    
    dynamote = zmq.Context()
    tv_req = dynamote.socket(zmq.REQ)
    tv_push = dynamote.socket(zmq.PUSH)
    tv_sub = dynamote.socket(zmq.SUB)
    tv_pub = dynamote.socket(zmq.PUB)
    tv_rep = dynamote.socket(zmq.REP)
    


    def ready_to_process(self,port_stb):
        
        #   Autoconfiguration and ip_address for connect is 169.254.1.3 on the port 5001
        ip_address = str("169.254.1.3")
        default_port = "5001"

        if len (sys.argv)>1:
            port = sys.argv[1]
            int(port)

        if len(sys.argv) > 2:
            port1 = sys.argv[2]
            int(port1)

        if len(sys.argv) >3:
            port2 = sys.argv[3]
            int(port2)

        if len(sys.argv)>4:
            port3 = sys.argv[4]
            int(port3)

        tv_description ="TV is on this",ip_address,"and",default_port
        print (tv_description)

        #Connect link
        tv_req.connect("tcp://127.0.0.1:%s"%port_stb)
        print ("connected to the middleware", ".....")

        for request in range (2):
            msg_description = msgpack.packb(str(tv_description))
            print ("Sending message")
            tv_req.send(msg_description)
            #  Get the reply.
            reply = tv_req.recv()
            message_unpacked = msgpack.unpackb(reply)
            print ("Received reply ", request, "[", message_unpacked, "]")
            time.sleep(1)


        tv_rep = dynamote.socket(zmq.REP)
            # Bind link
        while True:
            tv_rep.bind("tcp://*:5001")
            msg = tv_rep.recv()
            print ("Got", msg)
            time.sleep(1)
    
###############################PUB###########################
    


################### function sending description ############

    def send():
        """Here is my description file, take care of it """
        try:
            tv_packed = msgpack.packb(str(open('tv-device-api-description.json','r')))
            tv_spec = dynamote.socket(zmq.PUSH)
            tv_spec.bind("tcp://*:5555")
            tv_spec.send(tv_packed)
        except IOError as e:
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))  
    ##################################################################
        
    def publish(self):
        
        print ("Publish to other process ...")
        tv_pub.bind("tcp://*:%s"%port)
        channel = ["channel1","channel2", "channel3","channel4"]
        mute = ["false", "true"]
        power = ["on", "off"]
        link_statement = ["stb", "DVD"]

        while True:
            msg_pub = choice (channel) + " " + choice (mute) + " " + choice (power) + choice (link_statement)
            print(">", msg_pub)
            socket.send(msg_pub)






























        
