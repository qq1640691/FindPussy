import os
import torch
from ultralytics import YOLO

from Tools_package.Tools_Pose import non_rectangular_crop
from Tools_package.Tools_YoloTestorMain import yolo_test


model_pussy = YOLO('TrainPT/V8X_D9900_T50.pt')
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model_pussy.to(device)
model_pose = YOLO("D:\PyWorkRoom\YoloV8-pose\yolov8x-pose.pt")
model_pose.to(device)
print("Using device: %s" % device)

if __name__ == '__main__':
    data_path = r"Test_Data"
    save_path_img = None
    confidence = 0.1
    iou = 0.5
    #最长边长
    max_size = 640 # 重绘图片保证显示时可以看到
    '''两个模型顺序别搞反了,参数依次是数据路径,姿态模型,pussy模型,图像保存路径,为空不保存,显示图片,置信度,iou,resize显示,filter表示是否对姿态和框选进行过滤,先大的部分'''
    yolo_test(data_path, model_pose=model_pose,model_pussy=model_pussy, save_path_img=save_path_img, confidence=confidence, iou=iou, resize=max_size,filter=True)
