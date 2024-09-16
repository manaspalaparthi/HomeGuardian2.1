import cv2
# import fast api
from fastapi import FastAPI, File, UploadFile, HTTPException , Security , APIRouter
from fastapi.responses import RedirectResponse
import uvicorn
import threading
#from yolov8faceOnnx.test import YOLOv8_face
import gradio as gr
import datetime
import base64
import datetime
from util.TextToSpeech import text_to_speech, play_audio
from DataCollection.camera import WebcamStream
#from DataCollection.VoiceCommands import *
import socket
import os
import requests


# Use a lock to prevent multiple threads accessing the camera simultaneously
video_stream_lock = threading.Lock()

class DataCollector:
    def __init__(self):
        self.camera = WebcamStream()
        self.camera.start()
        self.device_id = 0
        self.is_recording = False
        self.hostname = socket.gethostname()
        #self.ip_address = socket.gethostbyname(self.hostname)
        print("Hostname: " + self.hostname)

    def get_device_id(self):
        return f"""<h1> Device ID: {self.device_id}</h1>"""

    def genrate_output_file_name(self):
        return str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))+"__HG__"+ str(self.device_id) + '.mp4'
    def start_recording(self, fps=30):
        # change the button color to red
        self.start.update("Recording in progress",variant="primary")
        if not self.camera.is_recording:
            self.file_name = self.genrate_output_file_name()
            text_to_speech(f"Recording started!")
            return {self.camera.record(self.file_name)}
        return "Recording is already in progress"

    def stop_recording(self):

        if not self.camera.is_recording:
            return "No recording in progress"

        self.start.update("Start Recording",)

        self.camera.stop_record()

        # read the video file and upload to the s3 bucket
        with open(self.file_name, "rb") as video_file:
            files = {"file": (self.file_name, video_file, "video/mp4")}
            text_to_speech("recording stopped")
            response = requests.post("http://localhost:8000/upload/", files=files)
            if response.ok:
                print(response.json())
                return "Video uploaded successfully"
        return "Video upload failed"

    def live(self):

        while True:
            yield self.camera.html_str

    def gradio_live(self):
        # Create a custom Block for video streaming

        RTPS = gr.outputs.HTML(label="Video Stream")

        iface = gr.Interface(
            fn=self.live,
            inputs=None,
            outputs=gr.HTML(self.camera.html_str),
            allow_flagging="never",
        )

        with gr.Blocks() as block:

            gr.Markdown("# Home Guardian Video data collection")

            with gr.Column():
                # show the device ID

                device_id = gr.Markdown()

                gr.Markdown(f"## Host name: {self.hostname}")

                #gr.Markdown(f"## Device IP: {self.ip_address}")

                block.load(self.get_device_id,[],outputs=device_id)

                iface.render()

                gr.Markdown("## Video recording")

                # button to start recording and stop recording

                self.start = gr.Button("Start Recording")

                self.start.click(self.start_recording, outputs=gr.outputs.HTML(label="Video Stream"))

                self.stop  = gr.Button("Stop Recording")

                self.stop.click(self.stop_recording, outputs=gr.outputs.HTML(label="Video Stream"))

                refresh = gr.Button("Refresh")

                refresh.click(self.get_device_id, [], outputs=device_id)

                # infrared mode

                self.infrared =  gr.Radio(["On", "Off"], label ="Infrared Mode")

                # infrared toggle radio button

                self.infrared = gr.Radio(["On", "Off"], label="Infrared Mode")

                self.infrared.change(self.Toggle_infrared, self.infrared)


        return block.launch(server_name="0.0.0.0", server_port=8001,enable_queue= True)


    def Toggle_infrared(self,value):

        if value == "On":
            self.camera.Infrared_on()
        elif value == "Off":
            self.camera.Infrared_off()

        text_to_speech(f"Infrared mode {value}")

    def run_gradio_server(self):

        gradio_thread = threading.Thread(target=self.gradio_live)
        gradio_thread.start()
        print("gradio live started")


if __name__ == '__main__':
    video_stream = DataCollector()
    video_stream.run_gradio_server()

    # command_handler_thread = threading.Thread(target=start_speech_command_handler)
    # command_handler_thread.start()

    app = FastAPI()
    router = APIRouter()
    import boto3
    from dotenv import load_dotenv

    load_dotenv()


    # AWS S3 configuration
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_access_key = os.getenv("AWS_ACCESS_KEY")
    aws_bucket_name = os.getenv("AWS_BUCKET_NAME")

    print(aws_access_key_id, aws_access_key, aws_bucket_name)

    s3_client = boto3.client(
        's3',
        region_name='ap-southeast-2',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_access_key
    )


    @router.get("/")
    async def root():
        # redirect to docs http://127.0.0.1:8000/docs
        return RedirectResponse(url="/docs")

    @router.get("/start_recording")
    async def start_recording():
        return {"message":  video_stream.start_recording()}

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

        text_to_speech("Video uploaded successfully")
        return {"message": "Video uploaded successfully",
                "video_link": f"https://{aws_bucket_name}.s3.amazonaws.com/{filename}"}



    app.include_router(router)
    uvicorn.run(app, host="", port=8000)

