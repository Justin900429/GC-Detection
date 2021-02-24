# README

[![Build Status](https://travis-ci.com/Justin900429/GC-Detection.svg?branch=main)](https://travis-ci.com/Justin900429/GC-Detection) [![PyPI](https://img.shields.io/pypi/v/GCDetection)](https://pypi.org/project/GCDetection/) ![PyPI - License](https://img.shields.io/pypi/l/GCDetection)

## Introduction 
Although there are lots of **object detection applications**, most of the applications are **hard to deploy**. In our project, we aim at **creating an simple application** that user can easily do the object detection jobs. In one of our demonstration, we will **simulate a seismic disaster and use a drone to do the search and rescue with our application**. This demonstration can show the value of our project.

## Demonstration
![](https://i.imgur.com/qQ8ymkC.jpg)
- **Red region**
    Show the image which the camera captured and draw the bounding boxes of the certain objects
- **Orange region**
    Press this button to capture the right now image and save this image to certain root(Google Cloud or local)
- **Green region**
    Show which categories display in the red region
- **Blue region**
    Press this button to leave the GUI 


## Main Goals
- Quickly deploy the object detection application

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


## Usage 
Follow the [documentation](https://justin900429.github.io/GC-Detection/Usage) to set up everything.


## Authors
- Justin Ruan, justin900429@gmail.com
- Joyce Fang, objdoctor891213a@gmail.com

## LICENSE
Under [MIT](https://opensource.org/licenses/MIT) LICENCE, please check it [here](https://github.com/Justin900429/GC-Detection/blob/main/LICENSE.txt)

## How to contribute
Not open now.

## Get stuck?
Open an issue or send us the email!😎






