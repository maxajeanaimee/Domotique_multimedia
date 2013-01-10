
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


import sys
import zmq
import socket
import msgpack


class ampli():

    def __init__(self):
        global dynamote
        global ampli_req
        dynamote = zmq.Context()
        ampli_req = dynamote.socket(zmq.REQ)
        ampli_sub = dynamote.socket(zmq.SUB)
                
    
    def ready_to_process(self,port):

        #   Autoconfiguration
        # ip_address for connect is 169.254.1.5 on the port 5005
        ip_address = str("169.254.1.5")
        port1 = "5001"
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

        ampli_description ="Ampli is on this",ip_address,"and",port
        print (ampli_description)
        #Connect link
        ampli_req.connect("tcp://127.0.0.1:%s"%port)

        for request in range (2):
            msg_description = msgpack.packb(str(ampli_description))
            print ("Sending message")
            ampli_req.send(msg_description)
            #  Get the reply.
            message = ampli_req.recv()
            print ("Received reply ", request, "[", message, "]")


    ######### Subscription #################
    ## when the middleware receive a message entry_dvd=, it sends a message to the DVD ##################


    def subscribe_to_dvd(self,port):

        ampli_sub = dynamote.socket(zmq.SUB)
        ampli_sub.connect("tcp://127.0.0.1:%s"%port)
        topicfilter = "on"
        ampli_sub.setsockopt_unicode(zmq.SUBSCRIBE, topicfilter)
        while True:
            print ("Middleware sense the DVD",ampli_sub.recv())




