from djitellopy import Tello
import gc_detection

# Connect to tello using djitellopy package
tello = Tello(host="172.20.10.8")
tello.connect()

# Open the tello's camera
tello.streamon()

# Start the app
detect_window = gc_detection.Interface()


class Control:
    """Class for controlling the tello with keypress

    The drone can fly 8 direction and also the takeoff and land command.
    """

    @staticmethod
    def takeoff(event):
        tello.takeoff()

    @staticmethod
    def land(event):
        tello.land()

    @staticmethod
    def forward(event):
        tello.send_rc_control(0, 50, 0, 0)

    @staticmethod
    def backward(event):
        tello.send_rc_control(0, -50, 0, 0)

    @staticmethod
    def left(event):
        tello.send_rc_control(-30, 0, 0, 0)

    @staticmethod
    def right(event):
        tello.send_rc_control(30, 0, 0, 0)

    @staticmethod
    def right_front(event):
        tello.send_rc_control(30, 30, 0, 0)

    @staticmethod
    def left_front(event):
        tello.send_rc_control(-30, 30, 0, 0)

    @staticmethod
    def right_back(event):
        tello.send_rc_control(30, -30, 0, 0)

    @staticmethod
    def left_back(event):
        tello.send_rc_control(-30, -30, 0, 0)

    @staticmethod
    def stop(event):
        tello.send_rc_control(0, 0, 0, 0)


# Bind the key with tello control
detect_window.root.bind("t", Control.takeoff)
detect_window.root.bind("w", Control.forward)
detect_window.root.bind("s", Control.backward)
detect_window.root.bind("a", Control.left)
detect_window.root.bind("d", Control.right)
detect_window.root.bind("wd", Control.right_front)
detect_window.root.bind("wa", Control.left_front)
detect_window.root.bind("sd", Control.right_back)
detect_window.root.bind("sa", Control.left_back)
detect_window.root.bind("<KeyRelease>", Control.stop)
detect_window.root.bind("l", Control.land)

# Start running the detection function
detect_window.start()
tello.streamoff()
