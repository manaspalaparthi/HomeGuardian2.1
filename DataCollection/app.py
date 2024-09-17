# fastapi_app.py
import os
import socket
import threading
import datetime
from fastapi import FastAPI, File, UploadFile, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.responses import StreamingResponse
from util.TextToSpeech import play_audio
from DataCollection.camera import WebcamStream
import boto3
from dotenv import load_dotenv
import io
import cv2


# Initialize FastAPI app and router
app = FastAPI()
router = APIRouter()

# Load environment variables
load_dotenv()

# AWS S3 configuration
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_access_key = os.getenv("AWS_ACCESS_KEY")
aws_bucket_name = os.getenv("AWS_BUCKET_NAME")

s3_client = boto3.client(
    's3',
    region_name='ap-southeast-2',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=os.getenv("AWS_ACCESS_KEY")
)

# Use a lock to prevent multiple threads accessing the camera simultaneously
video_stream_lock = threading.Lock()

class DataCollector:
    def __init__(self):
        self.camera = WebcamStream()
        self.camera.start()
        self.device_id = 0
        self.is_recording = False
        self.hostname = socket.gethostname()
        print("Hostname: " + self.hostname)

    def genrate_output_file_name(self):
        return str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")) + "__HG__" + str(self.device_id) + '.mp4'

    def start_recording(self):
        if not self.camera.is_recording:
            self.file_name = self.genrate_output_file_name()
            play_audio("../wav/Recording_started.mp3")
            self.camera.record(self.file_name)
            return "Recording started"
        return "Recording is already in progress"

    def stop_recording(self):
        if not self.camera.is_recording:
            return "No recording in progress"

        self.camera.stop_record()
        play_audio("../wav/Recording_stopped.mp3")

        # Upload the video to S3
        with open(self.file_name, "rb") as video_file:
            s3_client.put_object(Bucket=aws_bucket_name, Key=self.file_name, Body=video_file)
            return "Video uploaded successfully"
        return "Video upload failed"

    def toggle_infrared(self, value):
        if value == "On":
            self.camera.Infrared_on()
            play_audio("wav/Infrared_on.mp3")
            return "Infrared mode turned on"
        elif value == "Off":
            self.camera.Infrared_off()
            play_audio("wav/Infrared_off.mp3")
            return "Infrared mode turned off"
        return "Invalid infrared mode"

# Create a single instance of DataCollector
video_stream = DataCollector()

# FastAPI routes
@router.get("/")
async def root():
    return RedirectResponse(url="/docs")

def generate_video_stream():
    while True:
        frame_encoded = video_stream.camera.encoded_frame
        frame_bytes = frame_encoded.tobytes()

        # Yield the frame with the correct content type for MJPEG
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Endpoint to serve the video stream
@router.get("/video_stream")
async def video_stream_endpoint():
    return StreamingResponse(generate_video_stream(), media_type='multipart/x-mixed-replace; boundary=frame')


@router.post("/toggle_infrared")
async def toggle_infrared(mode: str):
    return {"message": video_stream.toggle_infrared(mode)}

@router.get("/start_recording")
async def start_recording():
    return {"message": video_stream.start_recording()}

@router.get("/stop_recording")
async def stop_recording():
    return {"message": video_stream.stop_recording()}

@router.get("/assign_device_id")
async def assign_device_id(device_id: int):
    video_stream.device_id = device_id
    return {"message": f"Device ID assigned: {video_stream.device_id}"}

@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    file_content = await file.read()
    filename = file.filename
    s3_client.put_object(Bucket=aws_bucket_name, Key=filename, Body=file_content)

    play_audio("../wav/uploaded.mp3")
    return {"message": "Video uploaded successfully", "video_link": f"https://{aws_bucket_name}.s3.amazonaws.com/{filename}"}

# Include router
app.include_router(router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
