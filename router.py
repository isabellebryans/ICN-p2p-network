from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import json

class Router:
    def __init__(self, name,public_key,private_key):
        self.multi_request = 0
        self.name = name  # device name
        self.cs = dict()  # name: data: freshness
        self.pit = list(tuple())  # name
        self.fib = list(tuple())  # prefix, ip address, ongoing interface
        self.location = list(tuple()) #name, address, listen port, send port
        self.sensor_list = list()
        self.private_key = private_key
        self.public_key = public_key
        self.WaitingList = list(tuple()) # sensor name, time
      

        with open("interfaces.json", 'r') as load_f:
            load_dict = json.load(load_f)
        #Set location
        for i in range(len(load_dict)):
            if(name == list(load_dict[i].keys())[0]):
                details = load_dict[i][name]
                self.setLocation(name,details[0]["address"], details[0]["listen port"],
                                  details[0]["send port"])
        # get the current device's neighbours
        # print(self.name)
        neighbours_list = list()
        for i in range(len(load_dict)):
            device_name = list(load_dict[i].keys())[0]
            #print(device_name)
            if device_name == self.name:
                neighbours_dict = load_dict[i][device_name][1]  # neighbours dictionary
                neighbours_list = neighbours_dict[list(neighbours_dict.keys())[0]]  # neighbours list
                # set list of sensors
                if len(load_dict[i][device_name]) > 2:
                    sensor_dict = load_dict[i][device_name][2]
                    self.sensor_list = sensor_dict[list(sensor_dict.keys())[0]]
                    print("sensor list of {} is {}".format(self.name, self.sensor_list))

        

        # add neighbours into the current fib
        for neighbour_name in neighbours_list:
            for i in range(len(load_dict)):
                device_name = list(load_dict[i].keys())[0]
                if device_name == neighbour_name:
                    device_detail = load_dict[i][device_name][0]
                    listen_port = device_detail[list(device_detail.keys())[0]]
                    addr = device_detail[list(device_detail.keys())[2]]
                    self.setFib(device_name, addr, listen_port)

        # add sensor
        for i in range(len(load_dict)):
            sensor_name = list(load_dict[i].keys())[0]
            if sensor_name != name:
                if sensor_name.startswith(name):
                    sensor_list = load_dict[i][sensor_name][0]
                    listen_port = list(sensor_list.values())[0]
                    addr = list(sensor_list.values())[2]
                    self.setFib(sensor_name, addr, listen_port)


    def getSerialisedPublicKey(self):
        serialized_key = self.public_key.save_pkcs1(format='PEM')
        serialized_key = serialized_key.decode('utf-8')
        return serialized_key

    def getPublicKey(self):
        return self.public_key
    
    def getPrivateKey(self):
        return self.private_key
    
    def getName(self):
        return self.name

    def getCS(self):
        return self.cs
    
    def getSensors(self):
        return self.sensor_list
    
    def getWaitingList(self):
        return self.WaitingList
    
    def setWaitingList(self, sensor, time):
        self.WaitingList.append((sensor, time))
        return
        
    def popWaitingList(self,name,interface):
        self.WaitingList.remove((name,interface))

    # cache new data
    def setCS(self, name, data, freshness):
        self.cs[name] = [data,freshness]

    def getPit(self):
        return self.pit

    # record the incoming interface of Interest Packet
    # WHERE THE PACKET CAME FROM?
    def setPit(self, name, interface):  # incoming interface
        self.pit.append((name, interface))

    def popPit(self,name,interface):
        self.pit.remove((name,interface))

    def getFib(self):
        return self.fib

    def setLocation(self, name, address, listen_port,send_port):
        self.location = (name,address,listen_port,send_port)

    def getLocation(self):
        return self.location
    
    def getAddress(self,name):
        for address in self.fib:
            #print("Comparing name ", name, " with address in fib: ", address)
            if name == address[0]:
                return(address[1],address[2])

    # for scalable ????
    def setFib(self, prefix, addr, interface):  # ongoing interface
        t = (prefix, addr, interface)
        self.fib.append(tuple(t))

    def setMultiRequest(self):
        self.multi_request = 0

    def updateMultiRequest(self):
        self.multi_request +=1

    def getMultiRequest(self):
        return self.multi_request
    
    # Get list of neighbours that are rovers
    def getNeighbourRovers(self):
        neighbour_rovers = list(tuple())
        for k in range(len(self.fib)):
            fib_length = len(self.fib[k][0].split('/'))
            #print("neighbor = ", self.fib[k][0])
            if fib_length < 4:
                #print("neighbour being added to list of neighbour rovers")
                neighbour_rover = self.fib[k]
                neighbour_rovers.append(neighbour_rover)
            # else fib element is sensor
        return neighbour_rovers

    



   
