import cv2
import os

import numpy as np

'''显示图片比例为25,自己可以修改'''


def resize_image(image, scale_percent=25):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized


def draw_boxes_on_image(image_path, txt_path):
    """
    Draws bounding boxes on an image based on the coordinates provided in a text file.

    Parameters:
    - image_path (str): Path to the image file.
    - txt_path (str): Path to the corresponding text file with bounding box coordinates.
    """
    # Load the image
    # print(cv2.imread(image_path))
    with open(image_path, 'rb') as f:
        image = cv2.imdecode(np.frombuffer(f.read(), np.uint8), cv2.IMREAD_COLOR)

    # Read bounding box coordinates from the text file
    with open(txt_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            class_id, x_center, y_center, width, height = map(float, line.split())
            # Convert normalized coordinates to pixel coordinates
            img_width, img_height = image.shape[1], image.shape[0]
            x1 = int((x_center - width / 2) * img_width)
            y1 = int((y_center - height / 2) * img_height)
            x2 = int((x_center + width / 2) * img_width)
            y2 = int((y_center + height / 2) * img_height)
            # Draw the bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    print(image_path)
    return image


def display_images_with_boxes(image_directory, text_directory):
    image_files = sorted([f for f in os.listdir(image_directory) if
                          f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))])
    current_index = 0

    while True:
        if current_index >= len(image_files):
            break

        img_file = image_files[current_index]
        txt_file = os.path.splitext(img_file)[0] + ".txt"
        img_path = os.path.join(image_directory, img_file)
        txt_path = os.path.join(text_directory, txt_file)
        img_with_boxes = draw_boxes_on_image(img_path, txt_path)
        scale_percent = 15  # 缩放比例
        width = int(img_with_boxes.shape[1] * scale_percent / 100)
        height = int(img_with_boxes.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        resized = cv2.resize(img_with_boxes, dim, interpolation=cv2.INTER_AREA)
        cv2.imshow('Image with Bounding Boxes', resized)
        key = cv2.waitKey(0) & 0xFF
        if key == ord('q'):  # Press 'q' to quit
            break
        elif key == ord(' '):  # Press space to go to the next image
            current_index += 1
        elif key == ord('D'):  # Press right arrow key to go to the next image
            current_index += 1
        elif key == ord('A'):  # Press left arrow key to go to the previous image
            if current_index > 0:
                current_index -= 1

    cv2.destroyAllWindows()
