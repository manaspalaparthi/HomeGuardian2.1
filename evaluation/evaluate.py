import os
import cv2
from ultralytics import YOLO
import argparse
from models.yolov8faceOnnx.test import YOLOv8_face
import supervision as sv
class Evaluate:

    def __init__(self, model):

        #body detection model
        self.body_detection_model = YOLO("yolov8m.pt")

        self.model = model

        # annorate frames
        self.box_annotator = sv.BoxAnnotator(
            thickness=2,
            text_thickness=1,
            text_scale=0.5
        )

        # metrics
        self.miss_match_count= 0
        self.miss_match_frames = []
        self.total_frames = 0
        self.frame_count = 0

    def run(self, video_path):

        #open video stream
        cap = cv2.VideoCapture(video_path)
        self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print("Total frames in video: {}".format(self.total_frames))

        # loop over frames from the video file stream

        for result in self.body_detection_model.track(source=video_path, stream=True, agnostic_nms=True, conf=0.30, iou=0.7,
                                  tracker="bytetrack.yaml", persist=True):

            self.frame_count += 1
            frame = result.orig_img
            detections = sv.Detections.from_yolov8(result)
            detections.frame = frame

            # body count
            body_count, frame = self.count_people(result, detections, frame)

            # face count
            boxes, scores, classids, kpts = YOLOv8_face_detector.detect(frame)
            YOLOv8_face_detector.draw_detections(frame, boxes, scores,kpts)

            # count boxes
            face_count = len(boxes)

            if face_count != body_count:
                print(" Body count: {} Face count: {}".format( body_count, face_count))
                self.miss_match_count += 1
                self.save_frame(frame, self.frame_count, "mismatched_frames/")



            detections.frame = frame
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.result()
        cv2.destroyAllWindows()
        cap.release()

            # show the output frame
    def save_frame(self, frame, frame_id, output_path):

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        cv2.imwrite(output_path + "frame_"+str(frame_id)+".jpg", frame)
        print(f"Frame saved: {frame_id}")

    def count_people(self,result, detections, frame):

        if result.boxes.id is not None:
            detections.tracker_id = result.boxes.id.cpu().numpy().astype(int)

        detections = detections[(detections.class_id == 0)]

        labels = [
            f"{tracker_id} {self.body_detection_model.model.names[class_id]} {confidence:0.2f}"
            for _, _, confidence, class_id, tracker_id
            in detections
        ]
        self.box_annotator.annotate(
            scene=frame,
            detections=detections,
            labels=labels
        )

        return len(detections), frame

    def result(self):

        print("Total frames: {} Miss matched frames: {}".format(self.frame_count, self.miss_match_count))

        print("percentage of miss matched frames: {}".format((self.miss_match_count/self.frame_count)*100))

        print("Accuracy: {}".format(100 - ((self.miss_match_count/self.frame_count)*100)))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default='0', help="webcam")
    args = parser.parse_args()


    YOLOv8_face_detector = YOLOv8_face('../models/yolov8faceOnnx/weights/yolov8n-face.onnx', conf_thres= 0.45, iou_thres=0.5)
    # load evaluation class
    evaluate = Evaluate(YOLOv8_face_detector)
    # run evaluation
    evaluate.run(0)