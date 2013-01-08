
#
 # Copyright (C) 2012 ESIROI. All rights reserved.
 # Dynamote is free software: you can redistribute it and/or modify
 # it under the terms of the GNU General Public License as published by
 # the Free Software Foundation, either version 3 of the License, or
 # (at your option) any later version.
 
 # Dynamote is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 # GNU General Public License for more details.
 #
 # You should have received a copy of the GNU General Public License
 # along with Dynamote.  If not, see <http://www.gnu.org/licenses/>.
 #

import msgpack
import sys
import zmq
import time
import socket
from random import choice


class dvd():

    video_file = {"dvd_contenu","type", "duration"}
    power = ["on","off"]
    onpause = ["false", "true"]
    onrepeat = ["on", "off"]
    entry_dvd = ["false", "true"]
    
    def __init__(self,video_file,onpause):
        self.video_file = {"Pirate des caraibles", "mkv", "90"}
        power = "on"
        self.onpause = "true"
        self.onrepeat = "off"
        self.entry_dvd = "false"
                 

    global dynamote
    global dvd_req
    global dvd_sub
    global dvd_pub
    global dvd_rep

    
    dynamote = zmq.Context()
    dvd_req = dynamote.socket(zmq.REQ)
    dvd_sub = dynamote.socket(zmq.SUB)
    dvd_pub = dynamote.socket(zmq.PUB)
    dvd_rep = dynamote.socket(zmq.REP)
                             

    def ready_to_process(self,port_stb):
        
        #   Autoconfiguration , ip_address for connect is 169.254.1.4 on the port 5004
        ip_address = str("169.254.1.4")
        default_port = "5004"

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

        dvd_description ="dvd is on this",ip_address,"and",default_port
        print(dvd_description)

        #Connect link
        dvd_req.connect("tcp://localhost:%s"%port_stb)
        print("connected to the middleware", ".....")

        for request in range (2):
            msg_description = msgpack.packb(str(dvd_description))
            print ("Sending message")
            dvd_req.send(msg_description)
            #  Get the reply.
            reply = dvd_req.recv()
            message_unpacked = msgpack.unpackb(reply)
            print ("Received reply ", request, "[", message_unpacked, "]")
            time.sleep(1)


        # Discover node other than the stb
        dvd_rep = dynamote.socket(zmq.REP)
         #Bind link
        while True:
            dvd_rep.bind("tcp://*:%s"%default_port)
            msg = dvd_rep.recv()
            print ("Got", msg)
            time.sleep(1)

    ############################### Publish #####################################
    def publish(self):

        print ("Publish to other process ...")
        port_pub =  "5551"
        dvd_pub.bind("tcp://127.0.0.1:%s" %port_pub)
        entry_dvd = [ 'on','off']
        media = ['mp3', 'mp4', 'avi', 'mkv']
        while True:
            msg_pub = choice(entry_dvd) + " " + choice(media)
            print (" There is a DVD disc")
            dvd_pub.send_unicode(msg_pub)





















v
