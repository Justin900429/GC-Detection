# Interface

The class show the images detected in Detection class. Also, provide the function to upload the image to [Google Cloud Storage](https://cloud.google.com/storage/).

> [Link](https://github.com/Justin900429/GC-Detection/blob/a55d351daf9fd209b98516f98576e2fea82c4516/detection.py#L232) to the class

## Attributes
| Attributes  | Type              | Description                                                   |
| ----------- | ------------------|-----------------------------------------|
| `root`      | **tkinter.Tk**    | Root object from tkinter.               |
| `frame`     | **numpy.array**   | Image with bounding box and categories. |

## Constructor
### `#!python __init__(self, cfg: str = "cfg.yaml")`
* Args
    * `cfg`: Path to the **yaml** file. The parameters of the cfg file are listed [here](index.md).

## Method
### `#!python start(self)`
Start the tkinter to work. The code inside is simply `#!python self.root.mainloop()`