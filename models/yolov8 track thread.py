from queue import Queue
from threading import Thread
from ultralytics import YOLO
import cv2

model = YOLO("yolov8m.pt")
print("model loaded")

# create queue to store frames
frame_queue = Queue()

# use OpenCV to read the video frames and put them in the queue
cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('outputnew.mp4', fourcc, fps, (width, height))


# create a separate thread for the tracking process
def tracking_thread():
    while True:
        # get the next frame from the queue
        frame = frame_queue.get()
        if frame is None:
            # sentinel value indicating end of frames
            frame_queue.task_done()
            break

        print("started loop")

        # track the objects in the frame
        results = model.track(frame)

        # loop through the results and draw bounding boxes on the frame
        for result in results:
            boxes = result.boxes
            print("boxex", boxes)

            for box in boxes:
                id = box.id
                xyxy = box.xyxy
                frame = cv2.rectangle(frame, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), (0, 255, 0), 2)

        # write the output frame to the video file
        out.write(frame)

        # display the output frame
        # cv2.imshow('output', frame)

        # check for the 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_queue.task_done()

    # release the video capture and writer objects and destroy the windows
    cap.release()
    out.release()
    cv2.destroyAllWindows()


# start the tracking thread
thread = Thread(target=tracking_thread)
thread.start()

# loop through the video frames and put them into the queue
while True:
    ret, frame = cap.read()
    if not ret:
        # add sentinel value to indicate end of frames
        frame_queue.put(None)
        break
    frame_queue.put(frame)

# wait for all tasks in the queue to be completed
frame_queue.join()

# wait for the tracking thread to finish
thread.join()
