import cv2
# import fast api
from fastapi import FastAPI, APIRouter
from fastapi.responses import RedirectResponse
import uvicorn
import threading
#from yolov8faceOnnx.test import YOLOv8_face
import gradio as gr
import datetime
import base64
import datetime
from camera import WebcamStream


# Use a lock to prevent multiple threads accessing the camera simultaneously
video_stream_lock = threading.Lock()

template = 'index.html'

class DataCollector:
    def __init__(self):
        self.camera = WebcamStream()
        self.camera.start()
        self.device_id = 0
        self.is_recording = False

    def genrate_output_file_name(self):
        return str(datetime.datetime.now()) + str(self.device_id) + '_HG.mp4'
    def start_recording(self, fps=30):

        # change the button color to red
        self.start.update("Recording in progress",variant="primary")
        return {self.camera.record(self.genrate_output_file_name())}

    def stop_recording(self):

        self.start.update("Start Recording",)

        return {self.camera.stop_record()}

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

            gr.Markdown("## Home Guardian Video data collection")

            with gr.Column():
                # show the device ID
                gr.Markdown(f"### Device ID: {self.device_id}")

                iface.render()

                gr.Markdown("## Video recording")

                # button to start recording and stop recording

                self.start = gr.Button("Start Recording")

                self.start.click(self.start_recording, outputs=gr.outputs.HTML(label="Video Stream"))

                self.stop  = gr.Button("Stop Recording")

                self.stop.click(self.stop_recording, outputs=gr.outputs.HTML(label="Video Stream"))

        return block.launch(enable_queue=True)

    def run_server(self):

        gradio_thread = threading.Thread(target=self.gradio_live)
        gradio_thread.start()
        print("gradio live started")

if __name__ == '__main__':
    video_stream = DataCollector()
    video_stream.run_server()

    app = FastAPI()
    router = APIRouter()

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

    app.include_router(router)
    uvicorn.run(app, host="", port=8000)

