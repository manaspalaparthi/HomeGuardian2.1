import os
import cv2
from ultralytics import YOLO
import argparse
from models.yolov8faceOnnx.test import YOLOv8_face
import supervision as sv
from models.defacecv.Deface import deface
from models.defacecv.Deface.centerface import CenterFace

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

        self.output_path = "../data/missing_frames_deface_night_30/3/"

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def run(self, video_path):

        path = video_path.split(".mp4")[0]

        # file name
        file_name = video_path.split("/")[-1].split(".mp4")[0]

        if not os.path.exists(path):
            os.makedirs(path)

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
            body_count, image = self.count_people(result, detections, frame.copy())

            # face count

            image, face_count=  deface.frame_detect(frame.copy(), self.model, threshold=0.3,  replacewith='blur',
             mask_scale = 1.0,
                ellipse = False,
            draw_scores = False)


            if face_count != body_count:

                if face_count > body_count:
                    print(" Body count: {} Face count: {}".format(body_count, face_count))
                    self.miss_match_count += 1
                    self.save_frame(image, self.frame_count, self.output_path+file_name, "1")
                else:
                    print(" Body count: {} Face count: {}".format(body_count, face_count))
                    self.miss_match_count += 1
                    self.save_frame(image, self.frame_count, self.output_path+file_name, "2")


            detections.frame = frame
            cv2.imshow("Frame", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.result(file_name)
        cv2.destroyAllWindows()
        cap.release()

            # show the output frame
    def save_frame(self, frame, frame_id, output_path, scenario:str= "1"):

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        cv2.imwrite(output_path + "/frame_"+str(frame_id)+"_"+scenario+".jpg", frame)
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

    def result(self, path):

        print("Total frames: {} Miss matched frames: {}".format(self.frame_count, self.miss_match_count))

        print("percentage of miss matched frames: {}".format((self.miss_match_count/self.frame_count)*100))

        print("Accuracy: {}".format(100 - ((self.miss_match_count/self.frame_count)*100)))

        # create a file to save the results
        with open(self.output_path+path+".txt", "w") as f:
            f.write("Total frames: {} Miss matched frames: {}\n".format(self.frame_count, self.miss_match_count))
            f.write("percentage of miss matched frames: {}\n".format((self.miss_match_count/self.frame_count)*100))
            f.write("Accuracy: {}\n".format(100 - ((self.miss_match_count/self.frame_count)*100)))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default='0', help="webcam")
    args = parser.parse_args()

    # load face detection model

    centerface = CenterFace(in_shape=(640,480), backend="auto", override_execution_provider=None)

    # load evaluation class
    evaluate = Evaluate(centerface)

    folder_path = "../data/nigthmode/3/"

    # list of all the videos in the folder
    videos = os.listdir(folder_path)

    videos = [video for video in videos if video.endswith('.mp4')]
    print("Videos: {}".format(videos))


    for video in videos:
        video_path = folder_path + video
        print("Evaluating video: {}".format(video))
        # run evaluation
        print("video_path: {}".format(video_path))
        evaluate.run(video_path)
