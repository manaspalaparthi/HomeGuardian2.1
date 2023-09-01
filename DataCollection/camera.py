import cv2
import time # time library
from threading import Thread # library for multi-threading
import base64

# defining a helper class for implementing multi-threading
class WebcamStream(Thread):
    # initialization method
    def __init__(self, stream_id=0):
        self.stream_id = stream_id  # default is 0 for main camera

        self.html_str=""

        # opening video capture stream
        self.vcap = cv2.VideoCapture(self.stream_id)
        if self.vcap.isOpened() is False:
            print("[Exiting]: Error accessing webcam stream.")
            exit(0)
        fps_input_stream = int(self.vcap.get(60))  # hardware fps
        print("FPS of input stream: {}".format(fps_input_stream))

        # reading a single frame from vcap stream for initializing
        self.grabbed, self.frame = self.vcap.read()

        #frame size

        self.frame_width  = self.frame.shape[1]
        self.frame_height = self.frame.shape[0]

        if self.grabbed is False:
            print('[Exiting] No more frames to read')
            exit(0)
        # self.stopped is initialized to False
        self.stopped = True
        self.paused = False
        # thread instantiation
        self.t = Thread(target=self.update, args=())
        self.t.daemon = True  # daemon threads run in background
        self.is_recording = False

    def stop_thread(self):
        self.stopped = True
        self.t.join()
        print("Thread stopped.")

    # method to start thread
    def start(self):
        self.stopped = False
        self.t.start()

    # method passed to thread to read next available frame
    def update(self):

        try:
            while True:
                if self.stopped is True:
                    break

                cv2.waitKey(20)

                if self.paused is True:
                    cv2.waitKey(-1)

                self.grabbed, self.frame = self.vcap.read()

                _, encoded_frame = cv2.imencode(".jpg", self.frame)
                frame_base64 = base64.b64encode(encoded_frame).decode("utf-8")
                # Create an HTML string to display the video frame
                self.html_str = f'<img src="data:image/jpeg;base64,{frame_base64}" width="640" height="480">'

                if self.is_recording:
                    self.video_writer.write(self.frame)

                if self.grabbed is False:
                    print('[Exiting] No more frames to read')
                    self.stopped = True
                    break
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            self.stopped = True
            self.t.join()
        self.vcap.release()

    # method to return latest read frame
    def read(self):
        return self.frame

    # method to stop reading frames
    def stop(self):
        self.stopped = True

    def pause(self):
        self.paused = True

    def record(self, output_name):
        if self.is_recording:
            return "Recording is already in progress."
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.video_writer = cv2.VideoWriter(output_name, fourcc, 30, (self.frame_width, self.frame_height))
        self.is_recording = True
        return f"Recording started. Output file: {output_name}"

    def stop_record(self):

        if not self.is_recording:

            return "No recording in progress."
        self.video_writer.release()
        self.is_recording = False
        return "Recording stopped."


if __name__ == '__main__':
    WebcamStream().start()
