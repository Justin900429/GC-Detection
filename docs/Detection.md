# Detection

This class provide the function for obtaining the detected images.

> [Link](https://github.com/Justin900429/GC-Detection/blob/81e26190606a6a4dcc87b1564301972f377106bc/detection.py#L47) to the class


## Attributes
| Attributes  | Type               | Description                                                   |
| ----------- | -------------------|-------------------------------------------|
| `categories`| **dict**           | Count all the detected objects.           |
| `img`       | **numpy.array**    | Origin image get from the camera.         |
| `size`      | **tuple**          | Size of image.                            |
| `frame`     | **numpy.array**    | Image with bounding boxes and categories. |


## Constructor

### `#!python __init__(self, google_kit_json_path: str, categories: list, size: tuple = (640, 480), max_results: int = 10, camera=0)`

Create an instance from Detection class.

- **Args**
    * `google_kit_json_path`: Path for the Google API JSON file. To get the API file, please refer to [this page](https://cloud.google.com/vision/docs/setup#api) .
    * `categories`: Categories to be detected. All supported types can be found in [here](https://modelcards.withgoogle.com/object-detection#performance).
    * `size`: Size of the images and frames.
    * `max_results`: Maximum results for the response. It won't absolutely contain the wanted objects listed in `categories`. The categories being selected is controlled by the Google Server.
    * `camera`: Camera to be used. The backend function was using `cv2.VideoCapture` in **OpenCV**. Please refer to [this link](https://bit.ly/2ZdQnD5) for all the valid input.

## Method

### `#!python start(self)`
Start the object detection and open the camera.

### `#!python end(self)`
End the detection and release the camera.

## Logic
Below is a flow chart that shows the logic behind the class.  

<img src="https://i.imgur.com/4JMuXG6.png" width=500/>

## Example
```python
import gcdetection
import cv2

# Create detected class and start the detection
detection_class = gcdetection.Detection(google_kit_json_path="/path/to/json/file",
                                        categories=["Person", "Book"],
                                        size=(640, 480),
                                        max_results=10,
                                        camera=0)
detection_class.start()

# Show the original images and detected images
while True:
    # Obtain images
    ori_img = detection_class.img
    detected_img = detection_class.frame
    
    # Wait for key
    key = cv2.waitKey(30) & 0xff
    if key == 27: # ESC
        break
    
    # Show the images
    if ori_img is not None:
        cv2.imshow("Original image", ori_img)
    if detected_img is not None:
        cv2.imshow("Detected image", detected_img)

# Release the resources
detection_class.end()
cv2.destroyAllWindows()
```

For more example, please visit the [example repository](https://github.com/Justin900429/GC-Detection/tree/main/example). 




    