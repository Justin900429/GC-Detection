# Interface

The class show the images detected in Detection class. Also, provide the function to upload the image to [Google Cloud Storage](https://cloud.google.com/storage/).

> [Link](https://github.com/Justin900429/GC-Detection/blob/a55d351daf9fd209b98516f98576e2fea82c4516/detection.py#L232) to the class

## Attributes
| Attributes  | Type              | Description                             |
| ----------- | ----------------- | --------------------------------------- |
| `root`      | **tkinter.Tk**    | Root object from tkinter.               |
| `frame`     | **numpy.array**   | Image with bounding box and categories. |

## Constructor
### `#!python __init__(self, cfg: str = "cfg.yml")`
* **Args**
    * `cfg`: Path to the **yaml** file. The parameters of the cfg file are listed [here](/GC-Detection/Usage/#config-file).

## Method
### `#!python start(self)`
Start the tkinter to work. The code inside is simply `#!python self.root.mainloop()`

### `#!python extra_info(self, info: dict)`
Show the user-defined information. The layout and the composition will be rearranged.

## Example

```python
import gcdetection

# Create detection interface and start detecting
detect_window = gcdetection.Interface()
detect_window.start()
```

For more example, please visit the [example repository](https://github.com/Justin900429/GC-Detection/tree/main/example).

## Extensive usage.
User can access to the `root` [attribute](#attributes). Any method that can be used in **tkinter** can also be implemented here. Below are some examples that users can do.

- **Key binding**  

    [Documentation from tkinter](https://docs.python.org/3/library/tkinter.html#bindings-and-events)

    ```python
    import gcdetection
    ...
    detect_window = gcdetection.Interface()
    
    # Should specify the event arguments for tkinter to pass in
    def task(event):
        pass
    # Bind key "k" to function "task"
    detect_window.root.bind("k", task)
    ...
    ```

- **Continuing task**

    [Reference to the usage](https://www.geeksforgeeks.org/python-after-method-in-tkinter/)
    
    ```python
    import gcdetection
    ...
    detect_window = gcdetection.Interface()
    ...
    # Should specify the event arguments for tkinter to pass in
    def task(event):
        # TODO: Task to define
        detect_window.root.after(20, task)
    
    # Run the task every 20 milliseconds
    detect_window.root.after(20, task)
    # Bind key "k" to function "task"
    detect_window.root.bind("k", task)
    ...
    ```