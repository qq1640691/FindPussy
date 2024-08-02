import torch
from ultralytics import YOLO

from Tools_package.Tools_YoloTestorMain import yolo_main, yolo_pose

model_pussy = YOLO('TrainPT/V8X_D9900_T50.pt')
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model_pussy.to(device)
model_pose = YOLO("D:\PyWorkRoom\YoloV8-pose\yolov8x-pose.pt")
model_pose.to(device)
print("Using device: %s" % device)


# if __name__ == '__main__':
#     data_path = r"D:\迅雷下载"
#     save_path_img = 'Test_images'
#     save_path_video = 'Test_videos'
#     confidence = 0.5
#     iou = 0.5
#     # 最长边长
#     # max_size = 640
#     yolo_main(data_path, model_pussy, save_path_img, save_path_video, confidence, iou)


'''只能处理图片'''
if __name__ == '__main__':
    data_path = r"Test_Data"
    save_path_img = None
    confidence = 0.1
    yolo_pose(data_path, model_pose, model_pussy, save_path_img,confidence)

