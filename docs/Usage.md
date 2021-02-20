# Usage


## Prerequisite

1. **Activate the Cloud Vision API**  
    User should follow [this](https://cloud.google.com/vision/docs/setup) link to finish setting up the Cloud API.
2. **Create Cloud Storage bucket** {==(Can be ignored for not uploading images)==}  
    If the users want to upload the detected images to Google Cloud Storage, please refer to [this link](https://cloud.google.com/storage/docs/creating-buckets) for creating a bucket.

!!!success
    Users don't have to set up the environment written in the above first reference. The program will automatically set up the environment for you.

## Config file

!!!info
    To use the class `Interface`, you must set up the config file using the below template or from [here](https://github.com/Justin900429/GC-Detection/blob/main/cfg_template.yaml).

Below show the template of config file. The format of config file is `YAML`.

```yaml
---
# GOOGLE_APPLICATION_CREDENTIALS API
google-kit-json: "/path/to/google/kit/json"

# Google Cloud Storage bucket name.
# Set null for not uploading images
bucket: null

# Maximum return object
# Note: The result could not be controlled.
# To promise for the wanted result, I recommend to set the bigger value.
max_request: 10

# Output folder to save images
#  if not exists, the program will help you create one.
#  Set null for not saving on local
output_path: null

# Camera setting. It was controlled by cv2.VideoCapture
# See the documentation from OpenCV
# https://bit.ly/2ZdQnD5
camera: 0

# Size of images.
width: 640
height: 480

# Detection categories.
categories:
  - Person
  - Book
...
```

* `google-kit-json`  
    This json file can be obtained from the [prerequisite part](#prerequisite)
* `bucket`  
    The name of the bucket. For example, if the user create a bucket called **images**, then leave **images** in this field.
* `categories`  
    See the [categories part](#categories) 

After creating config file, users can use it as below.

```python
import gc_detection

interface = gc_detection.interface(cfg="/path/to/config/file")
interface.start()
```

## Categories
All the supported categories can be found in [here](https://modelcards.withgoogle.com/object-detection#performance). You can search the wanted category like below image.

![categories](https://i.imgur.com/u1etDtR.jpg)

## Cost

!!!warning
    The service of cloud vision is not free.
    
* Price per 1000 units

| First 1000 units/month  | Units 1001 - 5,000,000 / month  | Units 5,000,001 and higher / month |
| ----------------------- | ------------------------------- | -----------------------------------|
| **Free**                | **$2.25US**                     | **$1.50US**                          |

For more pricing information, please visit the [doc](https://cloud.google.com/vision/pricing#prices) of Vision API.