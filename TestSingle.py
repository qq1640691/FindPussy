import torch
from ultralytics import YOLO

from Tools_package.Tools_VI_Test import img_operate_test, video_operate_test

model_path = 'TrainPT/V8X_D9900_T50.pt'  # Change this to your YOLOv8 model's path
model = YOLO(model_path)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print("Using device: %s" % device)
model.to(device)

if __name__ == '__main__':
    path = r"C:\Users\16406\Desktop\Test_Image1.jpg"
    img_operate_test(path, model, 0.1, 0.5, 640)
    # video_operate_test(path, model, 0.1, 0.5, 640)
