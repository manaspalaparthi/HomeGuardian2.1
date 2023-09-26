import cv2
import numpy as np
import math
import argparse
from test import YOLOv8_face
from deep_sort_realtime.deepsort_tracker import DeepSort

# inferance script for running yolov8faceOnnx model
def run(args):
    tracker = DeepSort(max_age= 30,polygon= True)
    winName = 'Deep learning face detection use OpenCV'
    YOLOv8_face_detector = YOLOv8_face(args.modelpath, conf_thres=args.confThreshold, iou_thres=args.nmsThreshold)
    cam = cv2.VideoCapture(0)
    while True:
        ret, srcimg = cam.read()
        if not ret:
            break
        # Detect Objects
        boxes, scores, classids, kpts = YOLOv8_face_detector.detect(srcimg)

        # if len(boxes) > 0:
        #     tracks = tracker.update_tracks([boxes,scores,classids],frame=srcimg)  # bbs expected to be a list of detections, each in tuples of ( [left,top,w,h], confidence, detection_class )
        #     for track in tracks:
        #         if not track.is_confirmed():
        #             continue
        #         track_id = track.track_id
        #         ltrb = track.to_ltrb()
        #         print("tracker id ",track_id)
        # #apply blur to detections
        dstimg = YOLOv8_face_detector.draw_detections(srcimg, boxes, scores, kpts)
        cv2.imshow(winName, dstimg)
        cv2.namedWindow(winName, 0)
        if cv2.waitKey(1) == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default='0', help="webcam")
    parser.add_argument('--modelpath', type=str, default='weights/yolov8n-face.onnx',
                        help="onnx filepath")
    parser.add_argument('--confThreshold', default=0.45, type=float, help='class confidence')
    parser.add_argument('--nmsThreshold', default=0.5, type=float, help='nms iou thresh')
    args = parser.parse_args()
    run(args)