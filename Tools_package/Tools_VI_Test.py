# -*- coding: utf-8 -*-
import os
import time
import torch
import cv2


def video_operate_test(video_path, model, conf, iou, max_size):
    cap = cv2.VideoCapture(video_path)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Finished processing video.")
            break

        # 使用cv2.resize调整图像大小
        # 注意：第二个参数是（宽度，高度），这是一个常见的陷阱
        frame = adaptive_resize(frame, max_size)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        with torch.no_grad():
            results = model(frame_rgb, iou=iou, verbose=True, conf=conf)

        for result in results:
            boxes = result.boxes
            for box in boxes:
                if box.conf > 0.5:
                    x1, y1, x2, y2 = box.xyxy[0]
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(frame, result.names[int(box.cls)], (int(x1), int(y1) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    cv2.putText(frame, str(float(box.conf)), (int(x1), int(y1) - 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.imshow('Detected', frame)
        cv2.waitKey(1)
    cap.release()
    cv2.destroyAllWindows()


def create_directory(path):
    """Create directory if it does not exist."""
    if not os.path.exists(path):
        os.makedirs(path)


def adaptive_resize(frame, max_size):
    height, width = frame.shape[:2]
    scale = max_size / max(height, width)
    return cv2.resize(frame, None, fx=scale, fy=scale)

def img_operate_test(img_path, model, conf, iou, max_size):
    # Read image from path
    frame = cv2.imread(img_path)
    if frame is None:
        return
    frame = adaptive_resize(frame, max_size)
    # Convert BGR image to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Perform inference with the model
    with torch.no_grad():
        results = model(frame_rgb, iou=iou, conf=conf, verbose=False)
    # Process detections and display them on the image
    for result in results:
        boxes = result.boxes
        print("boxes:", boxes)
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = box.conf[0].item()
            # Draw bounding box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            # Add confidence label
            label = f"Conf: {conf:.2f}"
            cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    # Display the image with detections
    cv2.imshow('Detections', frame)
    # Wait for user input
    key = cv2.waitKey(0)
    # Check if space bar is pressed
    if key == 32:  # ASCII code for space
        print("Space bar was pressed. Exiting.")
        return  # Exit the function immediately when space is pressed
    return
