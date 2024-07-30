import os
import torch
from ultralytics import YOLO

from Tools_package.Tools_Test import is_video_or_image, img_operate_test, video_operate_test

model_path = 'TrainPT/V8X_D9900_T50.pt'  # Change this to your YOLOv8 model's path
model = YOLO(model_path)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print("Using device: %s" % device)
model.to(device)

if __name__ == '__main__':
    data_path = r"Test_Data"
    for filename in os.listdir(data_path):
        filepath = os.path.join(data_path, filename)
        print(filepath)
        if is_video_or_image(filepath) == 0:
            # 文件路径,模型,保存文件路径(可选,默认不保存),置信度,iou,缩放比例
            img_operate_test(filepath, model, 'Test_images', 0.001, 0.5, 0.5)
        # if is_video_or_image(filepath) == 1:
        #     # 文件路径,模型,保存文件路径(可选,默认不保存),置信度,iou,缩放比例
        #     video_operate_test(filepath, model, 'Test_videos', 0.5, 0.5, 1)
