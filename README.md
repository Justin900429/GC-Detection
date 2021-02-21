# README

[![Build Status](https://travis-ci.com/Justin900429/GC-Detection.svg?branch=main)](https://travis-ci.com/Justin900429/GC-Detection)

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
- Detect certain obejects
- Search and rescue with drone
- 

## Where to get it
```
pip install GCDetection
```

## Needed Package
* [For mac](https://github.com/Justin900429/GC-Detection/blob/main/requirements/mac.txt)
```
pip install requirements/mac.txt
```

* [For others](https://github.com/Justin900429/GC-Detection/blob/main/requirements/common.txt)
```
pip install requirements/common.txt
```


## Usage 
Follow the [documentation](https://justin900429.github.io/GC-Detection/Usage) to set up everything.

## Example to Control the Drone
| | direction | arrow |
| :--------:| :--------: | :--------: |
| w | forward | &uarr; | 
| s | backward | &darr; |
| a | left | &larr; |
| d | right | &rarr; |
| w + d | right front | <img src="https://render.githubusercontent.com/render/math?math=\nearrow"> |
| w + a | left front | <img src="https://render.githubusercontent.com/render/math?math=\nwarrow"> |
| s + d | right rear | <img src="https://render.githubusercontent.com/render/math?math=\searrow"> |
| s + a | left rear | <img src="https://render.githubusercontent.com/render/math?math=\swarrow"> |
| t | take off |  |
| l | landing |  |
| Key Release| stop | |

## How to contribute
Not open now.

## Get stucked?
Open an issue or send the email!😎






