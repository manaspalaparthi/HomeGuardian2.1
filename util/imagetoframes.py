import numpy
import cv2
import argparse
import os

## write a function that take a path to a video file and convert it to frames and save it in a folder


def video_to_frames(video_path, frames_path):
    """
    This function takes a path to a video file and convert it to frames and save it in a folder
    :param video_path: path to the video file
    :param frames_path: path to the folder to save the frames
    :return: None
    """
    # create a VideoCapture object
    vidcap = cv2.VideoCapture(video_path)

    # create folder to save frames
    if not os.path.exists(frames_path):
        os.makedirs(frames_path)

    # read frames
    while vidcap.isOpened():
        success, frame = vidcap.read()
        if not success:
            break
        # save frame as JPEG file, where the name is 6 digit frame count left padded with 0s
        cv2.imwrite(frames_path + "/frame_%06d.jpg" % (int(vidcap.get(cv2.CAP_PROP_POS_FRAMES))-1),frame)


    # release the video capture object
    vidcap.release()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--video_path', type=str, default='data/1.mp4', help='path to the video file')
    parser.add_argument('--frames_path', type=str, default='data/frames', help='path to the folder to save the frames')
    args = parser.parse_args()
    video_to_frames(args.video_path, args.frames_path)