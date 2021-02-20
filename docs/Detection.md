# Detection

This class provide the function for obtaining the detected images.

> [Link](https://github.com/Justin900429/GC-Detection/blob/81e26190606a6a4dcc87b1564301972f377106bc/detection.py#L47) to the class


## Attributes
| Attributes  | Type                 | Description                                                   |
| ----------- | ---------------------|-----------------------------------------|
| `categories`| **dict()**           | Count all the detected objects.         |
| `img`       | **np.array()**       | Origin image get from camera.           |
| `size`      | **tuple()**          | Size of image.                          |
| `frame`     | **numpy.array()**    | Image with bounding box and categories. |


## Method

### `#!python start(self)`
Start the object detection and open the camera.

### `#!python end(self)`
End the detection and release the camera.

## Logic
Below is the flow char that shows the logic behind the class.
<img src="https://i.imgur.com/4JMuXG6.png" width=500/>


    