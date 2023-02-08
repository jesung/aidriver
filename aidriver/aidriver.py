import ac
import acsys
import sys
import os
import platform
import socket
from sim_info import info
# import time

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
l_x = 0
l_y = 0
l_z = 0
l_heading = 0
l_speed = 0
sock = None
flag = True
host = "127.0.0.1"  # The server's hostname or IP address
port = 65431  # The port used by the server


def acMain(ac_version):
    global l_x, l_y, l_z, l_heading, l_speed

    # create app and update visual settings
    app_window = ac.newApp("aidriver")
    ac.setSize(app_window, 200, 200)
    ac.setBackgroundOpacity(app_window, 1.0)
    ac.setBackgroundColor(app_window, 255, 255, 255)
    ac.setFontSize(app_window, 40)
        
    # create labels and set their locations
    l_x = ac.addLabel(app_window, "X: ")
    l_y = ac.addLabel(app_window, "Y: ")
    l_z = ac.addLabel(app_window, "Z: ")
    l_heading = ac.addLabel(app_window, "Heading: ")
    l_speed = ac.addLabel(app_window, "Speed: ")
    ac.setPosition(l_x, 3, 30)
    ac.setPosition(l_y, 3, 60)
    ac.setPosition(l_z, 3, 90)
    ac.setPosition(l_heading, 3, 120)
    ac.setPosition(l_speed, 3, 150)
    ac.setFontSize(l_x, 30)
    ac.setFontSize(l_y, 30)
    ac.setFontSize(l_z, 30)
    ac.setFontSize(l_heading, 30)
    ac.setFontSize(l_speed, 30)
        
    return "AI driver"


def acUpdate(deltaT):
    global l_x, l_y, l_z, sock, host, port, flag, l_heading, l_speed
    
    # get updated states from game
    # world_position = ac.getCarState(0, acsys.CS.WorldPosition)
    world_position = ac.getCarState(ac.getFocusedCar(), acsys.CS.TyreContactPoint, acsys.WHEELS.FL)
    heading = info.physics.heading
    # pitch = info.physics.pitch
    # roll = info.physics.roll
    speed = ac.getCarState(0, acsys.CS.SpeedKMH)
    
    # display to app window
    x = "{value:.2f}".format(value=world_position[0])
    y = "{value:.2f}".format(value=world_position[1])
    z = "{value:.2f}".format(value=world_position[2])
    heading = "{value:.4f}".format(value=heading)   # range [-pi, pi]
    speed = "{value:.2f}".format(value=speed)
    ac.setText(l_x, x)   
    ac.setText(l_y, y)
    ac.setText(l_z, z)
    ac.setText(l_heading, heading)
    ac.setText(l_speed, speed)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # use flag to connect once
    if flag:
        try:
            # try connecting to socket server
            sock.connect((host, port))
            flag = False
        except:
            ac.console("Could not connect to host")
    else:
        try:
            # Send current world position and car state. Note that socket.sendall requires bytes
            sock.sendall(str.encode(x + ',' + y + ',' + z + ',' + heading + ',' + speed + ','))
            # data = sock.recv(1024)
            # ac.console(f"Received {data!r}")
        except:
            ac.console("Could not connect to host")
            
    # laptime = ac.getCarState(0, acsys.CS.LapTime)
    # ac.setText(laptime, "Laptime: {}".format(laptime))
    # velocity = info.physics.velocity
    # ac.console("velocity: {}, {}, {}".format(velocity[0], velocity[1], velocity[2]))


def acShutdown():
    # Clean up the connection
    connection.close()
