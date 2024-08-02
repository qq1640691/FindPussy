# -*- coding: utf-8 -*-
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


def adaptive_resize(frame, max_size):
    height, width = frame.shape[:2]
    scale = max_size / max(height, width)
    return cv2.resize(frame, None, fx=scale, fy=scale)

def img_operate_test_pose(frame, model, conf, iou):
    # Read image from path
    # print(frame.shape)
    if frame is None:
        return
    # frame = adaptive_resize(frame, max_size)
    # Convert BGR image to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Perform inference with the model
    with torch.no_grad():
        results = model(frame_rgb, iou=iou, conf=conf, verbose=False)
    # Process detections and display them on the image
    for result in results:
        boxes = result.boxes
        if conf == 0:  # Only process the box with the highest confidence if conf is set to 0
            max_conf_box = boxes[torch.argmax(boxes.conf)]
            x1, y1, x2, y2 = max_conf_box.xyxy[0].tolist()
            conf = max_conf_box.conf[0].item()
            # Draw bounding box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            # Add confidence label
            label = f"Conf: {conf:.2f}"
            cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            height, width = frame.shape[:2]
            x1_norm = x1 / width
            y1_norm = y1 / height
            x2_norm = x2 / width
            y2_norm = y2 / height
            # cv2.imshow('Detections', frame)
            # cv2.waitKey(0)
            return [conf, x1_norm, y1_norm, x2_norm, y2_norm]
