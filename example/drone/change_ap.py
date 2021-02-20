"""
This code is aim at connecting
tello to others wifi
"""

from djitellopy import Tello

# Connect to tello
tello = Tello()
tello.connect()

# Connect to other wifi
tello.connect_to_wifi("<ssid>", "<password>")
