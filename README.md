# GC Detection

[![Build Status](https://travis-ci.com/Justin900429/GC-Detection.svg?branch=main)](https://travis-ci.com/Justin900429/GC-Detection) [![PyPI](https://img.shields.io/pypi/v/GCDetection)](https://pypi.org/project/GCDetection/) ![PyPI - License](https://img.shields.io/pypi/l/GCDetection)

[![image](https://i.imgur.com/rUsc0qX.png)](https://youtu.be/X0PYE7MsEoc)

## Introduction 
Although there are lots of **object detection applications**, most of the applications are **hard to deploy**. In our project, we aim at **creating a simple application** that users can easily do the object detection jobs. In one of our demonstration, we used **drone to find out where the balls were and saved the images on Google Cloud**. This demonstration is a simple version of doing search and rescue. Namely, ball can be replaced with real people. This demonstration shows the value of our project.

## Objectives
There are three main objectives of our project.
1. Make object detection easier.
2. Used in the field of search and rescue.
3. Do the crowd counting.

## Interface layout
![](https://i.imgur.com/qQ8ymkC.jpg)
- **Red region**
    Show the image which the camera captured and draw the bounding boxes of the certain objects
- **Orange region**
    Press this button to capture the image and save image to certain root(Google Cloud or local)
- **Green region**
    Show which categories display in the red region
- **Blue region**
    Press this button to leave the GUI 

## Documentation
> Note: Although GC Detection is open source, using Google Cloud Vision API is not free. For more information, please refer to the documentation
>

Follow the [documentation](https://justin900429.github.io/GC-Detection/Usage) to set up everything.

## Installation
Before install the package, we highly recommend to build the virtual env. There are lots of tools user can choose. Below, we demonstrate how to use in conda environment.

```
conda create -n name-of-env python=3.8
conda activate name-of-env
```

- PyPI
```
pip install GCDetection
```

- Build from source
```
git clone https://github.com/Justin900429/GC-Detection.git
cd GC-Detection
pip install -e .
```

## Needed Package
* [For mac](https://github.com/Justin900429/GC-Detection/blob/main/requirements/mac.txt)
* [For others OS](https://github.com/Justin900429/GC-Detection/blob/main/requirements/common.txt)

## Authors
- Justin Ruan, justin900429@gmail.com
- Joyce Fang, objdoctor891213a@gmail.com

## LICENSE
Under [MIT](https://opensource.org/licenses/MIT) LICENCE, please check it [here](https://github.com/Justin900429/GC-Detection/blob/main/LICENSE.txt)

## How to contribute
pull request!

## Get stuck?
Open an issue or send us the email!😎

## User feedback
We really need the user feedback to help us promote the tools. Please fill [this form](https://forms.gle/VvnvQTCKrsLraNReA) to let us know how we can improve!






