import socket
import threading
import random
import json
import Interfaces
import time

bufferSize  = 1024
file = open('interfaces.json')
references = json.load(file)
Alive = True
AttributeList = ["repair_kit", "temperature","power", "volcanic_activity", "position", "humidity", "lidar", "pressure", "light", "soil_composition", "battery", "radiation", "camera"]
SensorList = ['RepairKit','LightSensor', 'PowerSensor', 'TemperatureSensor', 'HumiditySensor', 'LiDARSensor', 'LightSensor', 'RadiationSensor', 'AtmosphericPressureSensor', 'SoilCompositionSensor', 'VolcanicActivitySensor', 'PositionSensor', 'RoverCamera', 'Battery']



# NEED TO DO:
# Pop pit when 
# Send location data with data

#Finds the node with the given name in the reference json and returns its index
def find_node(name):
    for i in range(len(references)):
        if(name == list(references[i].keys())[0]):
            return i
    print("can't find node ", name)


########### Setup #########
def setup_sockets(listen_port,send_port):
    listen_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    send_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    print ("Socket successfully created")
    listen_socket.bind(('', listen_port))
    send_socket.bind(('',send_port))
    return listen_socket,send_socket

########## Update ##############
def update(socket, interface,router,name, lock):
    while Alive:
        # If sensor, update every 10 seconds
        if (interface.__class__.__name__ in SensorList):
            interface.update()
            #Update content store with data
            router.setCS(name,interface.data,time.time())
        else:
            # update position data in CS
            lock.acquire()
            update_position(router, socket)
            lock.release()
            # Check if sensor down
            for item in router.getWaitingList():
                if (float(time.time() - item[1])) > 10.0:
                    print("Sensor down!")
                    interest = 'repair_kit'
                    # Get neighbours of the node that are rovers, and choose randomly which one to send it to
                    neighbor = random.choice( router.getNeighbourRovers())
                    # Include the interest and the origin of the interest request
                    packet = (interest, name)
                    # Set the PIT 
                    router.setPit(interest, name)
                    socket.sendto(json.dumps(packet).encode(), (neighbor[1],neighbor[2]))
                    print("Interest {} sent to {}.".format(interest, neighbor))
                    router.popWaitingList(item[0], item[1])
                   # router.popPit()
        time.sleep(10)


def update_position(router, socket):
    sensor_name = router.getName() + "/position"
    #print("Getting location data ")
    # Get address of sensor
    address = router.getAddress(sensor_name)
    # Create data packet
    packet = ('position', router.getLocation()[0])
    #print("Forward to " + sensor_name)
    socket.sendto(json.dumps(packet).encode(), address)
    router.setPit('position', router.getName())
    return


########## Outbound #############
# Send interest packet
def outbound(socket,router,lock,node):
    global Alive
    while Alive:
        interest = input('Ask the network for information: ') 
        if interest == "Fail":
            #global Alive
            Alive = False
            print("Node dead. Alive is: ", Alive)
            exit(1)
        lock.acquire()
        # Get neighbours of the node that are rovers, and choose randomly which one to send it to
        neighbor = random.choice( router.getNeighbourRovers())
        # Include the interest and the origin of the interest request
        packet = (interest, node)
        # Set the PIT 
        router.setPit(interest, node)
        socket.sendto(json.dumps(packet).encode(), (neighbor[1],neighbor[2]))
        print("Interest {} sent to {}.".format(interest, neighbor))
        lock.release()
        


########## Inbound ##############
# check if the data in the CS is fresh, or old
def fresh(name, router):
    if name in router.getCS():
        if (float(time.time() - router.getCS()[name][1])) > 10.0:
            print("Stale")
            return False
        else:
            print("Fresh")
            return True 


# Handle Income Data Packet
def handle_packet(router, packet, socket):
    # decode packet
    packet = json.loads(packet.decode())
    #print("Packet recieved is: ", packet)
    #print(len(packet))
    # Data sent from another group
    if not isinstance(packet, list):
        print("Ignoring packet")
        return
    
    if packet[0] not in AttributeList:
        print("Ignoring packet")
        return

    need = packet[0]
    # INTEREST PACKET
    if len(packet) == 2:
        origin_node = packet[1] # origin

        print("Interest Packet Received! Interest packet is: ", packet)
        # If need in router.getCS() and fresh(need,router):
            #print("I have the Data!")
        
        current_interface = router.getName()
        
        # Sensor
        if len(current_interface.split("/")) == 4:      # If the node is a sensor
            print("router.getCS(): ", router.getCS())
            # Get the data from the sensors CS
            data = router.getCS()[router.getName()]
            packet = (need,data,router.getName())
            #print(data)
            # Get the address of the node that sent you the packet to sent it back
            address = router.getAddress(origin_node)
            # Sent data back to node that requested data
            print("Forward to " + origin_node)
            print(packet)
            print(type(packet))
            socket.sendto(json.dumps(packet).encode(), address) 
            return
        
        elif need in router.getCS() and fresh(need,router):
            print("I have the Data!")
            #Produce data packet name : data : freshness
            address = router.getAddress(origin_node)
            # need to change this to store location of where the data was gotten
            packet = (need,router.getCS()[need],origin_node)
            # print("Forward to " + interface)
            socket.sendto(json.dumps(packet).encode(), address)
            return
            
        # Node is not a sensor, but has the sensor needed
        elif need in router.getSensors():
            print("I have the right sensor!")
            # Get sensor name 
            sensor_name = router.getName() + "/" + need
            print("Sending interest packet to sensor ", sensor_name)
            # Get address of sensor
            address = router.getAddress(sensor_name)
            # Set the PIT
            router.setPit(need,origin_node)
            print("Updated pit. PIT: ", router.getPit())
            # Create data packet
            packet = (need, router.getLocation()[0])
            print("Forward to " + sensor_name)
            socket.sendto(json.dumps(packet).encode(), address)
            # SET TIMER?
            router.setWaitingList(sensor_name, time.time())
            return
        # Node does not have the sensor requires
        # Pass the data packet onto the next sensor
        elif packet not in router.getPit():
            print("I don't have the Data, sending on packet")
            # update pit
            router.setPit(need,origin_node)
            print("Updated pit. PIT: ", router.getPit())
            # send it to a neighbour rover node, but not where the data came from
            neighbors = router.getNeighbourRovers()
            print("Node's rover neighbours: ", neighbors)
            destination_node=[] # possible next destination nodes to send the packet onto
            # Filter out "neighbours" that are this node itself, and Bases
            # Don't want to send it to bases yet because haven't implemented that part yet

            for neighbor in neighbors:
                if neighbor[0] != origin_node:
                    destination_node.append(neighbor)
            print("destination nodes: ", destination_node)
            # choose a random one if there are more than one
            if len(destination_node) >1:
                destination_node = random.choice(destination_node)
            else:
                destination_node = destination_node[0]
            packet = (need, router.getLocation()[0])
            print("Forwarding to ", destination_node)
            socket.sendto(json.dumps(packet).encode(),(destination_node[1],destination_node[2]))
            return

    # DATA PACKET
    else:
        print("Data packet Received!")
        data = packet[1]
        inPit = False
        # Remove elements from waitlist
        for item in router.getWaitingList():
            if item[0] == packet[2]:
                router.popWaitingList(item[0], item[1])
                print("Deleting item from WaitingList. WaitingList: ", router.getWaitingList())
                
        #Remove elements in PIT which contain interest
        for interest in router.getPit(): 
            if interest[0] == need:
                #print("Satisfying interest table")
                router.popPit(interest[0],interest[1])
                #print("PIT popped. PIT: ", router.getPit())

                # Send data packet back to requesters
                if interest[1] != router.name:
                    address = router.getAddress(interest[1])
                    socket.sendto(json.dumps(packet).encode(), address)
                inPit = True
        if inPit:
            print("Popped from PIT. New PIT: ", router.getPit())
            print("Updating Content store")
            print("adding data: ", data)
            print("packet: ", packet)
        
            router.setCS(need,data[0],data[1])
            print("CS is now: ", router.getCS())
            return
        else:
            print("Not in interest table, ignore packet.")
            return
    
    return

# Listen for incoming datagrams
def inbound(socket,name,lock,router):
    while Alive:
        bytesAddressPair = socket.recvfrom(bufferSize)
        lock.acquire()
        message = bytesAddressPair[0]
        handle_packet(router,message,socket)
        lock.release()
        if not Alive:
            exit(1)


class p2p_node():
    def __init__(self,name,router,interface):
        #Interface name
        self.name = name

        #Thread Mutex
        self.lock = threading.Lock()

        #Set router and interface class
        self.router = router
        self.interface = interface

        #Find network details from json
        index=find_node(name)   
        network_details = references[index][name]
        self.listen_port = network_details[0]["listen port"]
        self.send_port = network_details[0]["send port"]
        self.address = network_details[0]["address"]
    
    def run(self):
        #setup inbound and outbound ports
        s_inbound,s_outbound= setup_sockets(self.listen_port,self.send_port)
        # creating thread
        t1 = threading.Thread(target=inbound, args=(s_inbound,self.name,self.lock,self.router))
        t2 = threading.Thread(target=outbound, args=(s_outbound,self.router,self.lock,self.name))
        t3 = threading.Thread(target=update, args=(s_outbound, self.interface,self.router,self.name, self.lock))

        # starting thread 1
        t1.start()
        # starting thread 2
        t2.start()
        # starting thread 3
        t3.start()
    
        # wait until thread 1 is completely executed
        t1.join()
        # wait until thread 2 is completely executed
        t2.join()

        t3.join()
