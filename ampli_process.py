import sys
import zmq
import socket
import msgpack

dynamote = zmq.Context()
ampli_req = dynamote.socket(zmq.REQ)

#   Autoconfiguration
# ip_address for connect is 169.254.1.5 on the port 5005
ip_address = str("169.254.1.5")
port = "5005"
port = "5001"
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
######### Subscription #################
## when the middleware receive a message entry_dvd=, it sends a message to the DVD ##################
    
ampli_sub = dynamote.socket(zmq.SUB)
ampli_sub.connect("tcp://127.0.0.1:5551")
ampli_pub.setsockopt_unicode(zmq.SUBSCRIBE, "on")
while True:
    print (ampli_sub.recv())




