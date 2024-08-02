import torch
from ultralytics import YOLO


from Tools_package.Tools_VI_Test import img_operate_test

model_pussy = YOLO('TrainPT/V8X_D9900_T50.pt')
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print("Using device: %s" % device)
model_pussy.to(device)



if __name__ == '__main__':
    img_operate_test(r"Test_Data/Test_Image4_2.jpg", model_pussy, 0, 0.5)