# Overview

Links to the [documentation](https://justin900429.github.io/GC-Detection/)

## Introduction
This project is for users to quickly deployed their object detection application. The backend used [Google Cloud Vision API](https://cloud.google.com/vision/) for object detection. The release now can only used the built in object detection trained by Google. In the future release, we will add [Google AutoML](https://cloud.google.com/automl) to fulfill costumed needs.

## Classes
The library contain two classes for use:  

* [Detection](/GC-Detection/Detection)  
    Get the images with bounding boxes on it.
      
* [Interface](/GC-Detection/Interface)  
    This class supports the GUI interface for the detection images and allows user to upload images to [Google Cloud Storage](https://cloud.google.com/storage/).

## Installation
Before install the package, we highly recommend to build the virtual env. There are lots of tools user can choose. Below, we demonstrate how to use in conda environment.

```
conda create -n <name-of-env> python=3.8
conda activate <name-of-env>
```

* PyPI

    ```commandline
    pip install GCDetection
    ```
 
* Build from source

    ```commandline
    git clone https://github.com/Justin900429/GC-Detection.git
    cd GC-Detection
    pip install -e .
    ```

## Usage
This page show the detail of using the GC_Detection package. [GO form here](/GC-Detection/Usage).

## Example Code
The example code was upload to the github directory, please visit [here](https://github.com/Justin900429/GC-Detection/tree/main/example).

