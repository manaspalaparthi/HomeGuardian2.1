import cv2
import multiprocessing
import time


def webcam_stream(output_queue):
    # Open the webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Read the current frame from the webcam
        ret, frame = cap.read()

        # Check if frame was successfully read
        if not ret:
            break

        # Put the frame into the output queue
        output_queue.put(frame)

    # Release the webcam and close the output queue
    cap.release()
    output_queue.close()


## process 1
def process_frame(frame_queue):
    # Process the frame here (e.g., perform some image manipulation)
    while True:
        frame = frame_queue.get()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Processed Frame', gray_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

## process 2
def process_frame_rgb(frame_queue):
    # Process the frame here (e.g., perform some image manipulation)

   # defacecv.run()

    while True:
        frame = frame_queue.get()
        cv2.imshow('Processed Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    # Create a multiprocessing Queue to share frames between processes
    frame_queue = multiprocessing.Queue()

    # Create and start the webcam process
    webcam_process = multiprocessing.Process(target=webcam_stream, args=(frame_queue,))
    webcam_process.start()


    process = multiprocessing.Process(target=process_frame, args=(frame_queue,))
    process.start()

    process_rgb = multiprocessing.Process(target=process_frame_rgb, args=(frame_queue,))
    process_rgb.start()

    time.sleep(30)

    # Terminate the webcam and frame processing processes
    webcam_process.terminate()
    webcam_process.join()

    process.terminate()
    process.join()

    process_rgb.terminate()
    process_rgb.join()

# Release resources
cv2.destroyAllWindows()