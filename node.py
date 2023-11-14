import argparse
import random
from UDPNode1 import p2p_node
from router import Router
import Interfaces as RI #roverInterfaces

def initialize_position():
    # Random position generation for rover
    return [random.randint(0, 500), random.randint(0, 500), random.randint(0, 200)]

def create_sensor_or_rover(interface_name):
    components = interface_name.split('/')
    component_length = len(components)

    if component_length == 4:
        sensor_type = components[3]
        return instantiate_sensor(sensor_type)
    else:
        entity_type = components[1]
        return instantiate_entity(entity_type, interface_name)

def instantiate_sensor(sensor_type):
    # Create instances of sensors based on type
    sensor_map = {
        'temperature': RI.TemperatureSensor,
        'humidity': RI.HumiditySensor,
        'lidar': RI.LiDARSensor,
        'light': RI.LightSensor,
        'soil_composition': RI.SoilCompositionSensor,
        'pressure': RI.AtmosphericPressureSensor,
        'radiation': RI.RadiationSensor,
        'camera': RI.RoverCamera,
        'battery': RI.Battery,
        'position': RI.PositionSensor,
        'volcanic_activity': RI.VolcanicActivitySensor,
        'power': RI.PowerSensor
    }
    return sensor_map.get(sensor_type, lambda: None)()

def instantiate_entity(entity_type, identifier):
    # Create rover or satellite base instances
    if entity_type == 'rovers':
        return RI.Rover(identifier)
    elif entity_type == 'bases':
        return RI.Base(identifier)
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Initialize a Mars Rover node')
    parser.add_argument('--name', type=str, help='Identifier for the node')
    args = parser.parse_args()

    if args.name is None:
        print("Node identifier is required.")
        exit(1)

    com_router = Router(args.name)
    node_entity = create_sensor_or_rover(args.name)
    mars_node = p2p_node(args.name, com_router, node_entity)
    mars_node.run()
