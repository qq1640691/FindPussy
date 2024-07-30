import os
import time
import torch
import cv2


def video_operate_test(video_path, model, save_path, conf, iou, resize):
    cap = cv2.VideoCapture(video_path)
    frame_num = 0
    create_directory(save_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Finished processing video.")
            break

        height, width = frame.shape[:2]
        # 计算新的尺寸
        new_width = int(width * resize)
        new_height = int(height * resize)
        # 使用cv2.resize调整图像大小
        # 注意：第二个参数是（宽度，高度），这是一个常见的陷阱
        frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
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
        frame_num += 1
        predix = int(time.time_ns())
        # 保存截图,可选
        # cv2.imwrite(f'{save_path}\\{predix}_{frame_num}.jpg', frame)
        cv2.imshow('Detected', frame)
        cv2.waitKey(1)
    cap.release()
    cv2.destroyAllWindows()


def create_directory(path):
    """Create directory if it does not exist."""
    if not os.path.exists(path):
        os.makedirs(path)


def img_operate_test(img_path, model, save_path, conf, iou, resize):
    # Get list of all images in the directory
    # Initialize index for image list
    # Read image from path
    create_directory(save_path)
    filename = os.path.basename(img_path)
    frame = cv2.imread(img_path)
    frame = cv2.resize(frame, (0, 0), fx=resize, fy=resize)
    # Convert BGR image to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Perform inference with the model
    with torch.no_grad():
        results = model(frame_rgb, iou=iou, conf=conf, verbose=False)
    # Process detections and display them on the image
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = box.conf[0].item()
            # Draw bounding box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            # Add confidence label
            label = f"Conf: {conf:.2f}"
            cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    # Display the image with detections
    predix = int(time.time_ns())
    # 保存截图,可选
    cv2.imwrite(f'{save_path}/{predix}_{filename}.jpg', frame)
    cv2.imshow('Detections', frame)
    # Wait for user input
    key = cv2.waitKey(0)
    # Check if space bar is pressed
    if key == 32:  # ASCII code for space
        print("Space bar was pressed. Exiting.")
        return  # Exit the function immediately when space is pressed
    return


def is_video_or_image(filename):
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv']
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

    _, ext = os.path.splitext(filename)

    if ext.lower() in video_extensions:
        return 1
    elif ext.lower() in image_extensions:
        return 0
    else:
        return -1
