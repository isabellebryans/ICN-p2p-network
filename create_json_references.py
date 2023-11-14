import json

Addresses = ["10.35.70.1", "10.35.70.9"]

Networks = ["rovers", "bases"]

Rovers = ["rover1","rover2","rover3","rover4","rover5"]
RoverNeighborList = [["/rovers/rover5","/rovers/rover2","/bases/base1"], ["/rovers/rover1","/rovers/rover3"], ["/rovers/rover2", "/rovers/rover4"], ["/rovers/rover3","/rovers/rover5", "/bases/base1"], ["/rovers/rover4","/rovers/rover1"]]

Bases = ["base1"]

Sensors = ["temperature", "volcanic_activity", "position", "humidity", "lidar", "pressure", "light", "soil_composition", "battery", "radiation", "camera"]

#baseSensors = ["shipradar", "fauna", "optimizer", "winds", "windd", "temperature", "precipitation", "alert"]
BaseNeighborList = [["/rovers/rover1","/rovers/rover4"]]

RoverSensorList = [["position", "camera", "battery", "temperature", "humidity", "pressure", "lidar", "light"], 
                   ["position", "camera", "battery", "temperature", "humidity", "pressure", "volcanic_activity", "soil_composition"],
                   ["position", "camera", "battery", "temperature", "humidity", "pressure", "radiation", "volcanic_activity"],
                   ["position", "camera", "battery", "temperature", "pressure", "lidar", "light", "radiation"],
                   ["position", "camera", "battery", "humidity", "pressure", "soil_composition", "lidar", "light"]]

json_array = []

listen_port = 33001
send_port = 33002
neighbor_itertator = 0
for rover in Rovers:
    rover_name = "/" + Networks[0] + "/" + rover
    json_array.append({rover_name : [{"listen port": listen_port,"send port": send_port,"address": Addresses[0]},{"neighbors" : RoverNeighborList[neighbor_itertator]}, {"sensors": RoverSensorList[neighbor_itertator]}]})
    listen_port += 2
    send_port += 2
    neighbor_itertator +=1
    for sensor in RoverSensorList[Rovers.index(rover)]:
        json_array.append({"/" + Networks[0] + "/" + rover + "/" + sensor : [{"listen port": listen_port,"send port": send_port,"address": Addresses[0]},{"neighbors" : [rover_name]}]})
        listen_port += 2
        send_port += 2

neighbor_itertator = 0
for base in Bases:
    base_name = "/" + Networks[1] + "/" + base
    json_array.append({base_name : [{"listen port": listen_port,"send port": send_port,"address": Addresses[1]},{"neighbors" : BaseNeighborList[neighbor_itertator]}]})
    listen_port += 2
    send_port += 2


with open('interfaces.json', 'w') as f:
  json.dump(json_array, f, indent=4)

