from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO(model="D:\PyWorkRoom\Yolov8\yolov8x.yaml", task='detect')
    results = model.train(
        data='pussy.yaml',
        device='0',
        epochs=100,
        batch=9,
        verbose=True,
        imgsz=640)
