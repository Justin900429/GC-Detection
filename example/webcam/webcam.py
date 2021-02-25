import gcdetection

# Record the running time
time = 1

# Additional task
def task(run_time):
    """Task to run in main loop"""
    info = {"time": f"{run_time}s"}
    detect_window.extra_info(info)
    detect_window.root.after(1000, task, run_time + 1)


# Start the app
detect_window = gcdetection.Interface()

# Assign task
detect_window.root.after(1000, task, time)

detect_window.start()
