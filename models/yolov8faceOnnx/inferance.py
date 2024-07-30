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
    cam = cv2.VideoCapture(args.source)

    ## save video same as input
    out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (int(cam.get(3)),int(cam.get(4))))

    ## video frame rate 30 fps
    cam.set(cv2.CAP_PROP_FPS, 30)


    while True:
        ret, srcimg = cam.read()
        if not ret:
            break
        # Detect Objects
        boxes, scores, classids, kpts = YOLOv8_face_detector.detect(srcimg)
        # #apply blur to detections
        dstimg = YOLOv8_face_detector.blur_detections(srcimg, boxes, scores, kpts)

        ## rgb to bgr


        ## save video
        out.write(dstimg)
        cv2.imshow(winName, dstimg)
        cv2.namedWindow(winName, 0)
        if cv2.waitKey(32) == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()
    out.release()
    print("Done")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default='video.mp4', help="webcam")
    parser.add_argument('--modelpath', type=str, default='weights/yolov8n-face.onnx',
                        help="onnx filepath")
    parser.add_argument('--confThreshold', default=0.45, type=float, help='class confidence')
    parser.add_argument('--nmsThreshold', default=0.5, type=float, help='nms iou thresh')
    args = parser.parse_args()
    run(args)