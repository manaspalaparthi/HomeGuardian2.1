import cv2
from flask import Flask, Response, render_template
import threading
from models.yolov8faceOnnx import YOLOv8_face
from flask_basicauth import BasicAuth

# Use a lock to prevent multiple threads accessing the camera simultaneously
class VideoStream:
    def __init__(self):
        self.video_stream_lock = threading.Lock()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        #self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        #self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.YOLOv8_face_detector = YOLOv8_face("../models/yolov8faceOnnx/weights/yolov8n-face.onnx", conf_thres=0.45, iou_thres=0.5)

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        with self.video_stream_lock:
            ret, frame = self.cap.read()
            if ret:
                # Detect Objects
                boxes, scores, classids, kpts = self.YOLOv8_face_detector.detect(frame)
                #apply blur to detections
                frame = self.YOLOv8_face_detector.blur_detections(frame, boxes, scores, kpts)
                _, encoded_frame = cv2.imencode(".jpg", frame)
                return encoded_frame.tobytes()
            else:
                return None

class streaming:

    def __init__(self):

        self.video_stream = VideoStream()
        app = Flask(__name__)
        self.app.route('/')
        self.app.route('/stop')
        self.app.route('/start')
        self.app.route('/video_feed')

        # authentification
        self.app.config['BASIC_AUTH_USERNAME'] = 'admin'
        self.app.config['BASIC_AUTH_PASSWORD'] = 'admin'
        self.app.config['BASIC_AUTH_FORCE'] = True
        self.basic_auth = BasicAuth(self.app)

    @app.route('/')
    def index(self):
        return render_template('index.html')

    def generate_frames(self):
        while True:
            frame = self.video_stream.get_frame()
            if frame is not None:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    @app.route('/video_feed')
    def video_feed(self):
        return Response(self.generate_frames(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/stop')
    def stop(self):
        self.video_stream.__del__()
        return render_template('index.html')

    @app.route('/start')
    def start(self):
        self.video_stream = VideoStream()
        return render_template('index.html')

    def run(self):
        self.app.run(debug=True, host='', port=5000)

if __name__ == '__main__':
    stream = streaming()
    stream.run()
