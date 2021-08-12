from .RaspbeeLights import RaspbeeLights as lights

if __name__ == "__main__":
    conbee = lights("yourConfigPath")
    print(lights.getRooms())

