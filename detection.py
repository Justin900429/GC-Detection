r"""This module is to give user a quickly built object detection application

Detection:
    This class provide the object detection function which use Google CLoud Vision API
    and can get the frame with bounding boxes on it.

Interface:
    This class provide how a GUI for user to save images and see the detected
    images. It can connect to Google Cloud Storage for saving the images being detected.
    To set the options, please use cfg_template.yaml as template.
"""

# Import built-in library
from collections import defaultdict
import threading
import sys
import os
import logging
import tkinter as tk
import datetime
import random
import platform
import io

import numpy as np
import yaml
# Import the Google Cloud client library
from google.cloud import vision
from google.cloud import storage
# Import image
import cv2
from PIL import Image
from PIL import ImageTk

if platform.system() == "Darwin":
    import tkmacosx

# Set up logger format
HANDLER = logging.StreamHandler()
FORMAT = logging.Formatter('[%(levelname)s] %(filename)s - %(lineno)d - %(message)s')
HANDLER.setFormatter(FORMAT)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(HANDLER)
LOGGER.setLevel(logging.INFO)


class Detection:
    def __init__(self,
                 google_kit_json_path: str,
                 categories: list,
                 size=(640, 480),
                 max_results: int = 10,
                 camera=0
                 ):
        # Check for the env
        if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") is None:
            LOGGER.info("Environment: 'GOOGLE_APPLICATION_CREDENTIALS' is not exist added to the "
                        "environment now...")
            # Path is not none and the path is given
            try:
                if (google_kit_json_path is None) or \
                        (not os.path.isfile(google_kit_json_path)):
                    LOGGER.error("The path given is not exist or the path is not given, "
                                 "please check the path")
                    raise FileNotFoundError  # Raise error

                # Add environment
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_kit_json_path
                LOGGER.info("Success added to the environment!")
            except FileNotFoundError:
                LOGGER.error("Error when adding the credentials, exit now..."
                             "Please check the given path.")
                sys.exit(1)

        # Camera height and width
        self.__size = size
        self.__camera = camera

        # Initialize the cap
        self.__cap = None

        # Max results and categories to detect
        self.__categories = categories
        self.__show_categories = defaultdict(int)
        self.__max_results = max_results

        # Color setting, randomly generate color
        self.__colors = []
        for _ in range(len(self.__categories)):
            self.__colors.append((int(random.random() * 255),
                                  int(random.random() * 255),
                                  int(random.random() * 255)))

        # JSON info for object detection
        self.__detect_info = None

        # Original image
        #  and bounding box image
        self.__img = None
        self.__frame = None

        # Control the prediction
        self.__predict_start = False

        # Initializing threads
        detect_objs = threading.Thread(target=self._detect_objs,
                                       daemon=True)
        detect_objs.start()
        draw_rec = threading.Thread(target=self._draw_rec,
                                    daemon=True)
        draw_rec.start()
        read_img = threading.Thread(target=self._get_img,
                                    daemon=True)
        read_img.start()

    @property
    def categories(self):
        return self.__show_categories

    @property
    def frame(self):
        return self.__frame

    @property
    def img(self):
        return self.__img

    @property
    def size(self):
        return self.__size

    def _detect_objs(self):
        while True:
            # Wait for input images
            if (not self.__predict_start) or \
                    (self.__img is None):
                continue

            # Client for detection
            client = vision.ImageAnnotatorClient()

            # Encode image to binary
            _, img_buffer = cv2.imencode(".jpg", self.__img)
            img_bytes = img_buffer.tobytes()

            # Change to vision Image type
            image = vision.Image(content=img_bytes)
            # Detect Person
            self.__detect_info = client.object_localization(image=image,
                                                            max_results=self.__max_results
                                                            ).localized_object_annotations
            cv2.waitKey(30)

    def _get_img(self):
        # Read camera image
        while True:
            # Wait for prediction
            if not self.__predict_start:
                continue

            # Get current frame and
            #  check for success
            success, self.__img = self.__cap.read()
            if not success:
                continue

            self.__img = cv2.resize(self.__img, (self.__size[0], self.__size[1]))

    def _draw_rec(self):
        # Draw the bounding boxes to the frame
        while True:
            # Save
            temp_categories = defaultdict(int)

            if (self.__detect_info is None) or \
                    (self.__img is None):
                continue

            # Get the size of image
            width, height = self.__size
            # Get the copy from self.__img
            self.__frame = np.copy(self.__img)
            for info in self.__detect_info:
                # Get only the person detection
                for i in range(len(self.__categories)):
                    if info.name != self.__categories[i]:
                        continue
                    # Increase the amount of detected object
                    temp_categories[info.name] += 1

                    # Pick out the bounding vertices
                    top_right_x, top_right_y = \
                        int(info.bounding_poly.normalized_vertices[0].x * width), \
                        int(info.bounding_poly.normalized_vertices[0].y * height)
                    bottom_right_x, bottom_right_y = \
                        int(info.bounding_poly.normalized_vertices[2].x * width), \
                        int(info.bounding_poly.normalized_vertices[2].y * height)

                    # Draw bounding boxes and put the text
                    cv2.rectangle(self.__frame,
                                  (top_right_x, top_right_y),
                                  (bottom_right_x, bottom_right_y),
                                  self.__colors[i],
                                  2)
                    cv2.putText(self.__frame,
                                f"{info.name} {info.score:.2f}",
                                (top_right_x, top_right_y),
                                cv2.FONT_HERSHEY_TRIPLEX,
                                0.5,
                                self.__colors[i], 2)

            self.__show_categories = temp_categories

    def start(self):
        # Wake up the camera and set the size
        self.__cap = cv2.VideoCapture(self.__camera)
        self.__cap.set(3, self.__size[0])
        self.__cap.set(4, self.__size[1])

        # Check whether the camera is opened or not
        if not self.__cap.isOpened():
            LOGGER.error("The camera is not opened, please check the path or the device.")
        self.__predict_start = True

    def end(self):
        # Close the prediction and
        #  release the camera
        self.__predict_start = False
        self.__cap.release()


class Interface:
    def __init__(self,
                 cfg: str = "cfg.yaml"):
        # Parse yaml file
        with open(cfg, "r") as yaml_file:
            self.yaml = yaml.load(yaml_file, Loader=yaml.FullLoader)

        # Check for the output path
        if (self.yaml["output_path"] is not None) and \
                (not os.path.exists(self.yaml["output_path"])):
            os.makedirs(self.yaml["output_path"])
        elif (self.yaml["output_path"] is not None) and \
                not os.path.isdir(self.yaml["output_path"]):
            LOGGER.error("Provided output path is already exist and not a directory. "
                         "Please check for the input file.")
            sys.exit(1)

        # Image to show, init to None
        self.frame = None

        # Initialize the root window and image panel
        self.root = tk.Tk()
        self.panel = None

        # Set the minimum size of the Tkinter window
        self.root.minsize(850, 500)

        # Open the detection Path
        self.detect = Detection(google_kit_json_path=self.yaml["google-kit-json"],
                                categories=self.yaml["categories"],
                                size=(self.yaml["width"], self.yaml["height"]),
                                max_results=int(self.yaml["max_request"]),
                                camera=self.yaml["camera"],
                                )
        self.detect.start()

        # Check OS to make the design
        if platform.system() == "Darwin":
            # Design the button of "snapshot" for MACOSX
            snap_btn = tkmacosx.Button(self.root,
                                       text="Snapshot!",
                                       command=self.take_snapshot,
                                       padx=10,
                                       pady=10,
                                       bg="#EDD4B2")
            # Design the button of "quit" for MACOSX
            quit_btn = tkmacosx.Button(self.root,
                                       text='Quit',
                                       command=self.on_close,
                                       padx=10,
                                       pady=10,
                                       background="#D0A98F")
        else:
            # Design the button of "snapshot" for other OS
            snap_btn = tk.Button(self.root,
                                 text="Snapshot!",
                                 command=self.take_snapshot,
                                 padx=10,
                                 pady=10,
                                 bg="#EDD4B2")
            # Design the button of "quit" for other OS
            quit_btn = tk.Button(self.root,
                                 text='Quit',
                                 command=self.on_close,
                                 padx=10,
                                 pady=10,
                                 background="#D0A98F")

        snap_btn.grid(row=0,
                      column=1)

        # Design the label to display which categories show up on the screen
        self.info_label = tk.Label(bg="#DFBFA1",
                                   height=20,
                                   width=16,
                                   anchor="nw",
                                   padx=10,
                                   pady=10)
        self.info_label.grid(row=1,
                             column=1)

        quit_btn.grid(row=2,
                      column=1)

        # Quit the event and start the video loop
        self.quit = threading.Event()
        video_start = threading.Thread(target=self.video_loop,
                                       daemon=True)
        video_start.start()

        # Set a callback to handle when the window is closed
        self.root.wm_title("Object detection")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.on_close)

    def video_loop(self):
        # Keep looping over frames until we are instructed to stop
        while not self.quit.is_set():
            # Get the correct frame
            self.frame = self.detect.frame
            if self.frame is None:
                continue

            # Convert BGR color to RGB and
            #  make it to pillow format
            image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)

            # If the panel is not None, we need to initialize it
            if self.panel is None:
                self.panel = tk.Label(image=image)
                self.panel.image = image
                self.panel.grid(row=0,
                                column=0,
                                rowspan=3,
                                padx=10,
                                pady=10)
            else:  # Otherwise, simply update the panel
                self.panel.configure(image=image)
                self.panel.image = image

            # Output the detected categories
            text = ""
            for name, count in self.detect.categories.items():
                text = f"{name}: {count}\n"
            self.info_label.configure(text=text)

    def upload(self, filename):
        # Save to local path
        save_img = self.frame.copy()

        # Make the Google Cloud Storage client
        #  and set the storage path
        client = storage.Client()
        bucket = client.get_bucket(self.yaml["bucket"])
        image_blob = bucket.blob(filename)

        # Upload and save the image
        try:
            if self.yaml["output_path"] is not None:
                # Save image in local
                LOGGER.info("Saved {filename} in local folder",
                            filename=filename)
                path = os.path.sep.join((self.yaml["output_path"], filename))
                cv2.imwrite(path, save_img)

                # Upload to Google Cloud Storage
                #  if the user set the "bucket" option
                if self.yaml["bucket"] is not None:
                    image_blob.upload_from_filename(os.path.sep.join((self.yaml["output_path"],
                                                                      filename)),
                                                    content_type="image/jpeg")

                    LOGGER.info("Saved {filename} to google cloud storage",
                                filename=filename)
            elif self.yaml["bucket"] is not None:
                # Convert numpy array to bytes
                temp_file = Image.fromarray(cv2.cvtColor(save_img, cv2.COLOR_BGR2RGB))
                temp_file_bytes = io.BytesIO()
                temp_file.save(temp_file_bytes,
                               format="JPEG")

                # Read the bytes from beginning
                temp_file_bytes.seek(0)
                image_blob.upload_from_file(temp_file_bytes,
                                            content_type="image/jpeg")

                LOGGER.info("Saved {filename} to google cloud storage",
                            filename=filename)
        except Exception as error:
            # If errors occur, just print the error messages
            #  and don't exit the program
            LOGGER.warning(error)

    def take_snapshot(self):
        # Set the filename to
        #  year_month_date_hour_minute_second.jpg
        time_label = datetime.datetime.now()
        filename = f"{time_label.strftime('%Y-%m-%d_%H-%M-%S')}.jpg"

        # Start the saving function in background
        save_img_back = threading.Thread(target=self.upload,
                                         args=(filename,),
                                         daemon=True)
        save_img_back.start()

    def on_close(self):
        # Release the resource and
        #  close the windows
        LOGGER.info("closing...")
        self.quit.set()
        self.detect.end()
        self.root.quit()
