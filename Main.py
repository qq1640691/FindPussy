import torch
from ultralytics import YOLO

from Tools_package.Tools_YoloTestorMain import yolo_main

model_path = 'TrainPT/V8X_D9900_T50.pt'  # Change this to your YOLOv8 model's path
model = YOLO(model_path)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print("Using device: %s" % device)
model.to(device)

if __name__ == '__main__':
    data_path = r"D:\迅雷下载"
    save_path_img = 'Test_images'
    save_path_video = 'Test_videos'
    confidence = 0.5
    iou = 0.5
    # 最长边长
    # max_size = 640
    yolo_main(data_path, model, save_path_img, save_path_video, confidence, iou)
