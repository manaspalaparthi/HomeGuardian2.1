from ultralytics import YOLO

# Load an official or custom model
model = YOLO('weights/yolov8-lite-s.pt')  # Load an official Detect model
# Perform tracking with the model
results = model.track(source="https://youtu.be/Zgi9g1ksQHc", show=True)  # Tracking with default tracker
results = model.track(source="https://youtu.be/Zgi9g1ksQHc", show=True, tracker="bytetrack.yaml")  # Tracking with ByteTrack tracker