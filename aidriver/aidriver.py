import ac
import acsys
import sys
import os
import platform
import socket
from sim_info import info

try:
    if platform.architecture()[0] == "64bit":
        sysdir = "stdlib64"
    else:
        sysdir = "stdlib"

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "third_party", sysdir))
    os.environ['PATH'] = os.environ['PATH'] + ";."
except Exception as e:
    ac.log("AI Driver: Error importing libraries: %s" % e)


# declare global variables
l_x = None
l_y = None
l_z = None
l_heading = None
l_speed = None
l_position = None
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
flag = True
host = "127.0.0.1"  # The server's hostname or IP address
port = 65431  # The port used by the server


def acMain(ac_version):
    global l_x, l_y, l_z, l_heading, l_speed, l_position

    # create app and update visual settings
    app_window = ac.newApp("aidriver")
    ac.setSize(app_window, 200, 200)
    ac.setBackgroundOpacity(app_window, 0.8)
    ac.setBackgroundColor(app_window, 255, 255, 255)
    ac.setFontSize(app_window, 40)
        
    # create labels and set their locations
    l_x = ac.addLabel(app_window, "X: ")
    l_y = ac.addLabel(app_window, "Y: ")
    l_z = ac.addLabel(app_window, "Z: ")
    l_heading = ac.addLabel(app_window, "Heading: ")
    l_speed = ac.addLabel(app_window, "Speed: ")
    l_position = ac.addLabel(app_window, "Position: ")
    ac.setPosition(l_x, 3, 25)
    ac.setPosition(l_y, 3, 50)
    ac.setPosition(l_z, 3, 75)
    ac.setPosition(l_heading, 3, 100)
    ac.setPosition(l_speed, 3, 125)
    ac.setPosition(l_position, 3, 150)
        
    return "AI driver"


def acUpdate(deltaT):
    global l_x, l_y, l_z, sock, host, port, flag, l_heading, l_speed, l_position
    
    # get updated states from game
    # world_position = ac.getCarState(0, acsys.CS.WorldPosition)
    world_position = ac.getCarState(ac.getFocusedCar(), acsys.CS.TyreContactPoint, acsys.WHEELS.FL)
    heading = info.physics.heading
    # pitch = info.physics.pitch
    # roll = info.physics.roll
    speed = ac.getCarState(ac.getFocusedCar(), acsys.CS.SpeedKMH)
    position = ac.getCarState(ac.getFocusedCar(), acsys.CS.NormalizedSplinePosition)
    lap_time = ac.getCarState(ac.getFocusedCar(), acsys.CS.LapTime)
    throttle = ac.getCarState(ac.getFocusedCar(), acsys.CS.Gas)
    brake = ac.getCarState(ac.getFocusedCar(), acsys.CS.Brake)
    steer = ac.getCarState(ac.getFocusedCar(), acsys.CS.Steer)
    
    # display to app window
    x = "{value:.2f}".format(value=world_position[0])
    y = "{value:.2f}".format(value=world_position[1])
    z = "{value:.2f}".format(value=world_position[2])
    heading = "{value:.2f}".format(value=heading)   # range [-pi, pi]
    speed = "{value:.2f}".format(value=speed)
    position = "{value:.3f}".format(value=position)
    lap_time = "{value:d}".format(value=lap_time)
    throttle = "{value:.2f}".format(value=throttle)
    brake = "{value:.2f}".format(value=brake)
    steer = "{value:.2f}".format(value=steer)
    
    
    ac.setText(l_x, "X: " + x)   
    ac.setText(l_y, "Y: " + y)
    ac.setText(l_z, "Z: " + z)
    ac.setText(l_heading, "Heading: " + heading)
    ac.setText(l_speed, "Speed: " + speed)
    ac.setText(l_position, "Position: " + position)

    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # use flag to connect once
    if flag:
        try:
            # try connecting to socket server
            sock.connect((host, port))
            flag = False
            ac.console("AIDriver: Socket connection successful")
        except:
            ac.console("AIDriver: Could not connect to host")
    else:
        try:
            # Send current world position and car state. Note that socket.sendall requires bytes
            sock.sendall(str.encode(x + ',' + y + ',' + z + ',' + heading + ',' + speed + ',' + position + ',' + lap_time + ','
                                    + throttle + ',' + brake + ',' + steer + ','))
            # data = sock.recv(1024)
            # ac.console(f"Received {data!r}")
        except:
            pass
            # ac.console("AIDriver: Could not send data")
            
    # laptime = ac.getCarState(0, acsys.CS.LapTime)
    # ac.setText(laptime, "Laptime: {}".format(laptime))
    # velocity = info.physics.velocity
    # ac.console("velocity: {}, {}, {}".format(velocity[0], velocity[1], velocity[2]))


def acShutdown():
    # Clean up the connection
    connection.close()
