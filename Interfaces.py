import random 

import numpy as np 


def connect_sensor(self, prefix, interface):
    self.router.setPit(prefix, interface)

class Base:
    def __init__(self,id):
        self.data=id
    #classes of base: alert, Fauna, Optimizer, data, ShipRadar, Temperature, WindD, WindS
    def update(self):
        pass

class Rover:
    def __init__(self,id):
        self.data = id
    #classes of diver: Battery, Danger, Heart, Light, Oxygen, Position, Pressure, Radar
    def update(self):
        pass

class TemperatureSensor:
    def __init__(self):
        self.data= None

    def update(self):
        self.data = random.uniform(-80,20) #temperature range for mars surface area

    def get_temperature(self):
        #space for addition
        return self.data


class HumiditySensor:
    def __init__(self):
        self.data = None

    def update(self):
        self.data = random.uniform(0,10) # Mars has low humidity 

    def get_humidity(self):
        #logic for returning the humidity
        return self.data

class Battery:
    def __init__(self):
        self.data = None

    def update(self):
        self.data = random.uniform(0,100) # Mars has low humidity 

    def get_battery(self):
        #logic for returning the humidity
        return self.data

class LiDARSensor:
    def __init__(self):
        self.data = None

    def update(self):
        self.data = random.sample(range(100), 10)  # Sample terrain data

    def get_lidar_data(self):
        return self.data

class VolcanicActivitySensor:
    def __init__(self):
        self.data = None

    def update(self):
        self.data = random.sample(range(100), 10)  # Sample terrain data

    def get_volcanic_activity_data(self):
        return self.data
    
class PositionSensor:
    def __init__(self):
        self.x = random.randint(0, 500)
        self.y = random.randint(0, 500)
        self.z = random.randint(0, 200)
        self.data = np.array((self.x, self.y, self.z))
    def update(self):
        self.x = min(500, max(0, self.x + np.sign(0.5) * random.randint(0, 20)))
        self.y = min(500, max(0, self.y + np.sign(0.5) * random.randint(0, 20)))
        self.z = min(200, max(0, self.z + np.sign(0.5) * random.randint(0, 10)))
        self.data = np.array((self.x, self.y, self.z))

class LightSensor:
    def __init__(self):
        self.data = None

    def update(self):
        self.data = random.uniform(0, 1000)  # Light intensity in lux

    def get_light_intensity(self):
        return self.data


class SoilCompositionSensor:
    def __init__(self):
        self.data = None

    def update(self):
        self.data = {'Iron': random.uniform(0, 50),
                                 'Silicon': random.uniform(0, 50),
                                 'Aluminum': random.uniform(0, 50)}

    def get_soil_composition(self):
        return self.data


class AtmosphericPressureSensor:
    def __init__(self):
        self.data = None

    def update(self):
        self.data = random.uniform(0, 10)  # Pressure in hPa

    def get_pressure(self):
        return self.data

class RadiationSensor:
    def __init__(self):
        self.data = None

    def update(self):
        self.data = random.uniform(50, 500)  # Radiation level in mSv

    def get_radiation_level(self):
        return self.data

class PowerSensor:
    def __init__(self):
        self.data = None

    def update(self):
        self.data = random.uniform(0, 500)  # Radiation level in mSv


class RoverCamera:
    def __init__(self):
        self.data = None

    def update(self):
        self.data= "Image_" + str(random.randint(1, 1000)) # sort of placeholder for image sequence

    def get_camera_feed(self):
        return self.data
