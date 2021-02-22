import gcdetection
import cv2

# Create detected class and start the detection
detection_class = gcdetection.Detection(google_kit_json_path="/path/to/google/kit/json",
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
    if key == 27:  # ESC
        break

    # Show the images
    if ori_img is not None:
        cv2.imshow("Original image", ori_img)
    if detected_img is not None:
        cv2.imshow("Detected image", detected_img)

# Release the resources
detection_class.end()
cv2.destroyAllWindows()
