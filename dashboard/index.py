import gradio as gr

class Dashboard:
    def __init__(self):
        self.ip = "127.0.0.1" # IP address of the host machine
        self.port = 443 # Port number of the host machine


    def run(self):

        demo = self.live_data()
        demo.launch(share=True, debug=True,)

        pass

    def live_data(self):

        with gr.Blocks() as demo:
             gr.Video(value= "http://127.0.0.1:443/video_feed" ,label="Live Video Feed")

        return demo


if __name__ == '__main__':
    dashboard = Dashboard()
    dashboard.run()