from ultralytics import YOLO
import cv2


# Create the model
model = YOLO("yolov8l")

# Use the model
model.train(data="yoloconfig.yaml", epochs=10, device='mps')  # train the model
metrics = model.val()  # evaluate model performance on the validation set
# # model.export("yolo8mauto_annotation_v2.pt")  # export the model to a file

# load the model
#
# model = YOLO("/Users/manas/Documents/GitHub/HomeGuardian2.1/models/runs/detect/train13/weights/last.pt")
#
#
# #inference on a single image
#
# img = cv2.imread("/Users/manas/Documents/GitHub/HomeGuardian2.1/NearFallVideos/NearfallSampledv2/94ce733362654ccd79b13c4637396c6320d095c691cd5bb17a72b332cc6e4b8d.png")
#
# encoded_results = []
# for box in model(img)[0].boxes:
#     print(box.conf, box.cls, box.xyxy )
#     encoded_results.append({
#         'confidence': box.conf.item(),
#         'label': box.cls.item(),
#         'points': [
#             [box.xyxy[0][0].item(), box.xyxy[0][1].item(),
#             box.xyxy[0][2].item(), box.xyxy[0][3].item()]
#         ],
#         'type': 'rectangle'
#     })
#
# print(encoded_results)