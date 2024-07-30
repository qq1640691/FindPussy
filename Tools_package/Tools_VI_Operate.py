# -*- coding: utf-8 -*-
import os
import time
import torch
import cv2



def create_directory(path):
    """Create directory if it does not exist."""
    if not os.path.exists(path):
        os.makedirs(path)


def video_operate(video_path, model, save_path, conf, iou):
    cap = cv2.VideoCapture(video_path)
    frame_num = 0
    thepath = os.path.dirname(video_path).split("\\")[-1]
    create_directory(f"{save_path}\\{thepath}")
    while True:
        ret, frame = cap.read()
        height, width = frame.shape[:2]
        min_side = max(height, width)
        if not ret:
            print("Finished processing video.")
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        with torch.no_grad():
            results = model(frame_rgb, iou=iou, verbose=True, conf=conf)
        bbox_drawn = False
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = box.conf[0].item()
                # Draw bounding box
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), int(min_side * 0.003))
                # Add confidence label
                label = f"Conf: {conf:.2f}"
                cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX,max(min_side * 0.001, 0.5),
                            (0, 255, 0), max(int(min_side * 0.002), 2))
                bbox_drawn = True
        if bbox_drawn:
            predix = int(time.time_ns())
            # 保存截图,可选
            cv2.imwrite(f'{save_path}\\{thepath}\\{predix}_{frame_num}.jpg', frame)
        frame_num += 1
    cap.release()
    cv2.destroyAllWindows()


def img_operate(img_path, model, save_path, conf, iou):
    # Get list of all images in the directory
    print(img_path)
    thepath = os.path.dirname(img_path).split("\\")[-1]
    create_directory(f"{save_path}\\{thepath}")
    frame = cv2.imread(img_path)
    if frame is None:
        return
    height, width = frame.shape[:2]
    min_side = max(height, width)
    # frame = adaptive_resize(frame, max_size)
    # Convert BGR image to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Perform inference with the model
    with torch.no_grad():
        results = model(frame_rgb, iou=iou, conf=conf, verbose=True)
    # Process detections and display them on the image
    bbox_drawn = False
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = box.conf[0].item()
            # Draw bounding box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), int(min_side*0.003))
            # Add confidence label
            label = f"Conf: {conf:.2f}"
            cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, max(min_side*0.001, 0.5), (0, 255, 0), max(int(min_side*0.002), 2))
            bbox_drawn=True
    if bbox_drawn:
        # Display the image with detections
        predix = int(time.time_ns())
        # 保存截图,可选
        print(f'{save_path}\\{thepath}\\{predix}.jpg')
        cv2.imwrite(f'{save_path}\\{thepath}\\{predix}.jpg', frame)
    return
