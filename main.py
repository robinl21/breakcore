import cv2
from blob_detection import *
from draw_tools.draw_tools import *
import numpy as np

# Initialize webcam
cap = cv2.VideoCapture(0)

# Check if webcam opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

# Set webcam properties for better performance
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

circleBlobParams = CircleBlobParams()
circleBlobParams.detectParams.minArea = 500

drawParams = DrawParams()
drawParams.thickness = 3
drawParams.lineType = cv2.LINE_4
drawParams.color = (255, 255, 255)
drawParams.noise = (-10, 50)
drawParams.grain = (-250, 0)  

circleBlobDetector = CircleBlobDetector(circleBlobParams)

try:
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Can't receive frame from webcam")
            break

        # Detect blobs in the current frame
        keypoints = circleBlobDetector.detect(frame)

        # Draw detected blobs on the frame
        result = circleBlobDetector.drawKeypoints(frame, keypoints, drawParams)

        # Display the result
        cv2.imshow("Real-time Blob Detection", result)

        # Wait for key press and handle it
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("Quitting...")
            break
        elif key == ord('s'):
            # Save current frame
            cv2.imwrite('captured_frame.jpg', result)
            print("Frame saved as 'captured_frame.jpg'")

finally:
    # Release everything when job is finished
    cap.release()
    cv2.destroyAllWindows()
    print("DONE")