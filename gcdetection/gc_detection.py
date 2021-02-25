r"""This module is to give user a quickly built object detection application.

Detection:
    This class provide the object detection function which use Google CLoud Vision API
    and can get the frame with bounding boxes on it.

Interface:
    This class provide how a GUI for user to save images and see the detected
    images. It can connect to Google Cloud Storage for saving the images being detected.
    To set the options, please use cfg_template.yml as template.
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
    """Using the Cloud Vision API to get the detected images.

    Attributes:
        self.img: Original image get from camera.
        self.frame: Image with bounding boxes on it.
        self.size: Size of the image and frame.
        self.categories: Count the detected objects.

    Method:
        self.start(self): Start the detection.
        self.end(self): End the detection.
    """

    def __init__(self,
                 google_kit_json_path: str,
                 categories: list,
                 size: tuple = (640, 480),
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

        # Check for the size
        if len(size) != 2:
            LOGGER.error("The length of size should be 2, (width, height)")
            sys.exit(1)
        elif not isinstance(size[0], int) or \
                not isinstance(size[1], int):
            wrong_type = type(size[0]) if not isinstance(size[0], int) else type(size[1])
            LOGGER.error(f"The type of size should be integer not {wrong_type}.")
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
        detect_objs = threading.Thread(target=self.__detect_objs,
                                       daemon=True)
        detect_objs.start()
        draw_rec = threading.Thread(target=self.__draw_rec,
                                    daemon=True)
        draw_rec.start()
        read_img = threading.Thread(target=self.__get_img,
                                    daemon=True)
        read_img.start()

    @property
    def categories(self):
        """dict (name, count): Getter of detected categories."""
        return self.__show_categories

    @property
    def frame(self):
        """numpy.array: Getter of detected frame."""
        return self.__frame

    @property
    def img(self):
        """numpy.array: Getter of detected image."""
        return self.__img

    @property
    def size(self):
        """tuple (width, height): Size of the image and frame."""
        return self.__size

    def __detect_objs(self):
        """Get the detected information from Cloud Vision API
        and save the info in self.__detection_info.

        Args:
            self: Instance itself.

        Return: None
        """
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

    def __get_img(self):
        """Return the image from the camera.

        Args:
            self: Instance itself.

        Return: None
        """
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

    def __draw_rec(self):
        """Draw the bounding boxes and information
        on the self.__img.

        Args:
            self: Instance itself.

        Return: None
        """
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
        """Start the detection.

        Args:
            self: Instance itself.

        Return: None
        """

        # Wake up the camera and set the size
        self.__cap = cv2.VideoCapture(self.__camera)
        self.__cap.set(3, self.__size[0])
        self.__cap.set(4, self.__size[1])

        # Check whether the camera is opened or not
        if not self.__cap.isOpened():
            LOGGER.error("The camera is not opened, please check the input or the device.")
        self.__predict_start = True

    def end(self):
        """End the detection and release the resources.

        Args:
            self: Instance itself.

        Return: None
        """

        # Close the prediction and
        #  release the camera
        self.__predict_start = False
        self.__cap.release()


class Interface:
    """Design the Interface by tkinter and show information on it.

    Attributes:
        self.frame: Image with bounding boxes on it.
        self.root: Instance of tkinter.Tk().
        self.size: Size of the image.

    Method:
        self.start(self): Start the detection interface.
    """

    def __init__(self,
                 cfg: str = "cfg.yml"):
        # Parse yaml file
        with open(cfg, "r") as yaml_file:
            self.__yaml = yaml.load(yaml_file, Loader=yaml.FullLoader)

        # Check for the output path
        if (self.__yaml["output_path"] is not None) and \
                (not os.path.exists(self.__yaml["output_path"])):
            os.makedirs(self.__yaml["output_path"])
        elif (self.__yaml["output_path"] is not None) and \
                not os.path.isdir(self.__yaml["output_path"]):
            LOGGER.error("Provided output path is already exist and not a directory. "
                         "Please check for the input file.")
            sys.exit(1)

        # Image to show, init to None
        self.__frame = None

        # Initialize the root window and image panel
        self.root = tk.Tk()
        self.__panel = None

        # Set the minimum size of the Tkinter window
        self.root.minsize(850, 500)

        # Open the detection Path
        self.__detect = Detection(google_kit_json_path=self.__yaml["google-kit-json"],
                                  categories=self.__yaml["categories"],
                                  size=(self.__yaml["width"], self.__yaml["height"]),
                                  max_results=int(self.__yaml["max_request"]),
                                  camera=self.__yaml["camera"],
                                  )

        # Check OS to make the design
        if platform.system() == "Darwin":
            # Design the button of "snapshot" for MACOSX
            self.__snap_btn = tkmacosx.Button(self.root,
                                              text="Snapshot!",
                                              command=self.__take_snapshot,
                                              padx=10,
                                              pady=10,
                                              bg="#A8E0FF")
            # Design the button of "quit" for MACOSX
            self.__quit_btn = tkmacosx.Button(self.root,
                                              text='Quit',
                                              command=self.__on_close,
                                              padx=10,
                                              pady=10,
                                              background="#778EBB")
        else:
            # Design the button of "snapshot" for other OS
            self.__snap_btn = tk.Button(self.root,
                                        text="Snapshot!",
                                        command=self.__take_snapshot,
                                        padx=10,
                                        pady=10,
                                        bg="#A8E0FF")
            # Design the button of "quit" for other OS
            self.__quit_btn = tk.Button(self.root,
                                        text='Quit',
                                        command=self.__on_close,
                                        padx=10,
                                        pady=10,
                                        background="#778EBB")

        self.__snap_btn.grid(row=0,
                             column=1)

        self.__quit_btn.grid(row=3,
                             column=1)

        # Design the label to display which categories show up on the screen
        self.__info_label = tk.Label(bg="#8EE3F5",
                                     height=20,
                                     width=16,
                                     anchor="nw",
                                     padx=10,
                                     pady=10)
        self.__info_label.grid(row=1,
                               column=1)

        # Add user-defined label
        self.__user_define_label = tk.Label(bg="#70CAD1",
                                            height=10,
                                            width=16,
                                            anchor="nw",
                                            padx=10,
                                            pady=10)

        # Quit the event and start the video loop
        self.__quit = threading.Event()
        video_start = threading.Thread(target=self.__video_loop,
                                       daemon=True)
        video_start.start()

        # Set a callback to handle when the window is closed
        self.root.wm_title("Object detection")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.__on_close)

    @property
    def frame(self):
        """numpy.array: Getter of detected frame."""
        return self.__frame

    @property
    def size(self):
        """tuple (width, height): Size of the image and frame."""
        return self.__yaml["size"][0], self.__yaml["size"][1]

    def __video_loop(self):
        """Show the scene that the camera captured by using open CV.

        Args:
            self: Instance itself.

        Return: None
        """
        # Keep looping over frames until we are instructed to stop
        while not self.__quit.is_set():
            # Get the correct frame
            self.__frame = self.__detect.frame
            if self.__frame is None:
                continue

            # Convert BGR color to RGB and
            #  make it to pillow format
            image = cv2.cvtColor(self.__frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)

            # If the panel is not None, initialize it
            if self.__panel is None:
                self.__panel = tk.Label(image=image)
                self.__panel.image = image
                self.__panel.grid(row=0,
                                  column=0,
                                  rowspan=4,
                                  padx=10,
                                  pady=10)
            else:  # Otherwise, simply update the panel
                self.__panel.configure(image=image)
                self.__panel.image = image

            # Output the detected categories
            text = ""
            for name, count in self.__detect.categories.items():
                text = f"{name}: {count}\n"
            self.__info_label.configure(text=text)

    def __upload(self, filename):
        """Save image to both Cloud and local.

        Args:
            self: Instance itself.
            filename: The name of saved file.

        Return: None
        """
        # Save to local path
        save_img = self.__frame.copy()

        # Initialize the bucket for after usage
        image_blob = None

        # Make the Google Cloud Storage client
        #  and set the storage path
        if self.__yaml["bucket"] is not None:
            client = storage.Client()
            bucket = client.get_bucket(self.__yaml["bucket"])
            image_blob = bucket.blob(filename)

        # Upload and save the image
        try:
            if self.__yaml["output_path"] is not None:
                # Save image in local
                LOGGER.info(f"Saved {filename} in local folder", )
                path = os.path.sep.join((self.__yaml["output_path"], filename))
                cv2.imwrite(path, save_img)

                # Upload to Google Cloud Storage
                #  if the user set the "bucket" option
                if self.__yaml["bucket"] is not None:
                    image_blob.upload_from_filename(os.path.sep.join((self.__yaml["output_path"],
                                                                      filename)),
                                                    content_type="image/jpeg")

                    LOGGER.info(f"Saved {filename} to google cloud storage")
            elif self.__yaml["bucket"] is not None:
                # Convert numpy array to bytes
                temp_file = Image.fromarray(cv2.cvtColor(save_img, cv2.COLOR_BGR2RGB))
                temp_file_bytes = io.BytesIO()
                temp_file.save(temp_file_bytes,
                               format="JPEG")

                # Read the bytes from beginning
                temp_file_bytes.seek(0)
                image_blob.upload_from_file(temp_file_bytes,
                                            content_type="image/jpeg")

                LOGGER.info(f"Saved {filename} to google cloud storage")
        except Exception as error:
            # If errors occur, just print the error messages
            #  and don't exit the program
            LOGGER.warning(error)

    def __take_snapshot(self):
        """Take the current snapshot and call the upload function.

        Args:
            self: Instance itself.

        Return: None
        """
        # Set the filename to
        #  year_month_date_hour_minute_second.jpg
        time_label = datetime.datetime.now()
        filename = f"{time_label.strftime('%Y-%m-%d_%H-%M-%S')}.jpg"

        # Start the saving function in background
        save_img_back = threading.Thread(target=self.__upload,
                                         args=(filename,),
                                         daemon=True)
        save_img_back.start()

    def extra_info(self, info: dict):
        # Set up the label config
        self.__info_label.configure(height=10)
        self.__user_define_label.grid(row=2,
                                      column=1)

        # Put on the information
        text = ""
        for name, content in info.items():
            text = f"{name}: {content}\n"
        self.__user_define_label.configure(text=text)

    def start(self):
        """Start the GUI.

        Args:
            self: Instance itself.

        Return: None
        """
        self.__detect.start()
        self.root.mainloop()

    def __on_close(self):
        """End the GUI and release the resource.

        Args:
            self: Instance itself.

        Return: None
        """
        # Release the resource and
        #  close the windows
        LOGGER.info("closing...")
        self.__quit.set()
        self.__detect.end()
        self.root.quit()
