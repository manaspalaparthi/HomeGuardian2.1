# gradio_app.py
import gradio as gr
import requests
import socket
from fastapi import FastAPI
import io
from PIL import Image

class GradioApp:
    def __init__(self):
        self.hostname = socket.gethostname()
        self.fastapi_url = "http://localhost:8000"  # URL to the FastAPI server

    def get_device_id(self):
        response = requests.get(f"{self.fastapi_url}/assign_device_id?device_id=1")
        return response.json()["message"]

    def start_recording(self):
        response = requests.get(f"{self.fastapi_url}/start_recording")
        return response.json()["message"]

    def stop_recording(self):
        response = requests.get(f"{self.fastapi_url}/stop_recording")
        return response.json()["message"]

    def toggle_infrared(self, mode):
        response = requests.post(f"{self.fastapi_url}/toggle_infrared", json={"mode": mode})
        return response.json()["message"]

    def fetch_video_stream(self):
        # Return an HTML string that embeds the video stream from FastAPI
        stream_url = f"{self.fastapi_url}/video_stream"
        return stream_url

    def live(self, show_video):
        # Conditional rendering based on toggle state
        if show_video:
            iframe_html = f"""
                          <iframe src="{self.video_url}" width="1280" height="720" ></iframe>
                      """
        else:
            iframe_html = ""

        return iframe_html

    def gradio_live(self):
        self.video_url = self.fetch_video_stream()


        with gr.Blocks() as block:
            gr.Markdown("# Home Guardian Video Data Collection")

            device_id = gr.Markdown()

            gr.Markdown("# Home Guardian Video Live Stream")

            # Toggle button to show or hide the video stream
            show_video_toggle = gr.Checkbox(label="Show Video Stream", value=False)

            # HTML component to embed the video stream
            video_embed = gr.HTML()

            # Update the HTML component based on the toggle state
            show_video_toggle.change(self.live, inputs=show_video_toggle, outputs=video_embed)

            gr.Markdown("## Video Recording")

            self.start = gr.Button("Start Recording")
            self.start.click(self.start_recording, outputs=gr.outputs.HTML(label="Video Stream"))

            self.stop = gr.Button("Stop Recording")
            self.stop.click(self.stop_recording, outputs=gr.outputs.HTML(label="Video Stream"))

            refresh = gr.Button("Refresh")
            refresh.click(self.get_device_id, [], outputs=device_id)

            # Infrared mode toggle
            self.infrared = gr.Radio(["On", "Off"], label="Infrared Mode")
            self.infrared.change(self.toggle_infrared, inputs=self.infrared, outputs=gr.outputs.Textbox())

        block.launch(server_name="0.0.0.0", server_port=8001, enable_queue=True)

if __name__ == '__main__':
    gradio_app = GradioApp()
    gradio_app.gradio_live()
