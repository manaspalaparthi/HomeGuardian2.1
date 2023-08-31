import cv2
from flask import Flask, Response, render_template
import threading
from yolov8faceOnnx.test import YOLOv8_face
import gradio as gr
import datetime
import base64
import datetime
from camera import WebcamStream

app = Flask(__name__)
# Use a lock to prevent multiple threads accessing the camera simultaneously
video_stream_lock = threading.Lock()

template = 'index.html'

class VideoStream:
    def __init__(self):
        self.device_id = 0
        self.is_recording = False
        self.output_name = self.genrate_output_file_name()
        self.location = "VideoData/"

    def stop(self):
        self.cap.release()
    def start(self):
        self.cap = cv2.VideoCapture(0)
        self.YOLOv8_face_detector = YOLOv8_face("../yolov8faceOnnx/weights/yolov8n-face.onnx", conf_thres=0.45, iou_thres=0.5)
        self.gradio_run()

    def start_recording(self, fps=30):
        if not self.is_recording:

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            self.video_writer = cv2.VideoWriter(self.location + self.output_name, fourcc, fps, (1920,1080))
            self.is_recording = True
            print(f"Recording started. Output file: {self.output_name}")
        else:
            print("Recording is already in progress.")

    def genrate_output_file_name(self):
        return str(datetime.datetime.now()) + str(self.device_id) + '_HG.mp4'

    def stop_recording(self):
        if self.is_recording:
            self.video_writer.release()
            self.is_recording = False
            print("Recording stopped.")
        else:
            print("No recording in progress.")

    def get_frame(self):
        with video_stream_lock:
            while True:
                ret, frame = self.cap.read()
                if ret:
                    # Detect Objects
                    boxes, scores, classids, kpts = self.YOLOv8_face_detector.detect(frame)
                    #apply blur to detections
                    frame = self.YOLOv8_face_detector.blur_detections(frame, boxes, scores, kpts)
                    _, encoded_frame = cv2.imencode(".jpg", frame)
                    frame_base64 = base64.b64encode(encoded_frame).decode("utf-8")
                    # Create an HTML string to display the video frame
                    html_str = f'<img src="data:image/jpeg;base64,{frame_base64}" width="640" height="480">'

                    cv2.imshow("frame",frame)
                    # write the flipped frame
                    if self.is_recording:
                        self.video_writer.write(frame)

    def gradio_live(self):
        # Create a custom Block for video streaming

        RTPS = gr.outputs.HTML(label="Video Stream")

        # # ccs center the video
        # iface = gr.Interface(
        #     fn=self.get_frame,
        #     inputs=None,
        #     outputs=RTPS,
        #     live=True,
        #     allow_flagging="never",
        # )

        with gr.Blocks("Video Stream") as block:

            gr.Markdown("## Video Stream")

            with gr.Column():
                # show the device ID
                gr.Markdown(f"### Device ID: {self.device_id}")

                # iface.render()

                gr.Markdown("## Video recording")

                # button to start recording and stop recording

                gr.Button("Start Recording").click(self.start_recording)

                gr.Button("Stop Recording").click(self.stop_recording)

        return block.launch(enable_queue=True)

    def gradio_run(self):

        thread = threading.Thread(target=self.gradio_live)
        thread.daemon = False
        thread.start()
        print("gradio live started")

if __name__ == '__main__':
    video_stream = VideoStream()
    video_stream.start()

