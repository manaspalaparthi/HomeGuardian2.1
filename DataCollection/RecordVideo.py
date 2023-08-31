import cv2
from flask import Flask, Response, render_template
import threading
from yolov8faceOnnx.test import YOLOv8_face
from flask_basicauth import BasicAuth
from flask import Flask, Response, render_template
import datetime

app = Flask(__name__)

# Use a lock to prevent multiple threads accessing the camera simultaneously
video_stream_lock = threading.Lock()

template = 'index.html'

class VideoStream:
    def stop(self):
        self.cap.release()
    def start(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        #self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        #self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.YOLOv8_face_detector = YOLOv8_face("../yolov8faceOnnx/weights/yolov8n-face.onnx", conf_thres=0.45, iou_thres=0.5)

    def get_frame(self):
        with video_stream_lock:

            # save the video to a file if you want
            out = cv2.VideoWriter(str(datetime.datetime.now)+'_HG.avi', -1, 20.0, (640,480))

            ret, frame = self.cap.read()
            if ret:
                # Detect Objects
              #  boxes, scores, classids, kpts = self.YOLOv8_face_detector.detect(frame)
                #apply blur to detections
               # frame = self.YOLOv8_face_detector.blur_detections(frame, boxes, scores, kpts)

                _, encoded_frame = cv2.imencode(".jpg", frame)

                # write the flipped frame
                out.write(frame)
                return encoded_frame.tobytes()
            else:
                return None

video_stream = VideoStream()
def generate_frames():
    while True:
        frame = video_stream.get_frame()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop')
def stop():
    video_stream.stop()
    return render_template(template, message="Video Stopped")

@app.route('/start')
def start():
    video_stream.start()
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/')
def index():
    return render_template(template)

if __name__ == '__main__':

    app.config['BASIC_AUTH_USERNAME'] = 'admin'
    app.config['BASIC_AUTH_PASSWORD'] = 'admin'
    app.config['BASIC_AUTH_FORCE'] = True
    basic_auth = BasicAuth(app)

    app.run( host='0.0.0.0', port=443)
