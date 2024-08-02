import os
import time

import cv2
import numpy as np

from Tools_package.Tools_VI_Operate import create_directory
from Tools_package.Tools_VI_Test import img_operate_test_pose, adaptive_resize


def calculate_final_cropped_coordinates(w, h, *crops):
    """
    计算多次连续裁剪后的最终裁剪坐标。

    :param w: 原始图像宽度
    :param h: 原始图像高度
    :param crops: 可变数量的每次裁剪的归一化坐标 [x1, y1, x2, y2]
    :return: 最终裁剪坐标（以像素为单位）[x1, y1, x2, y2]
    """
    current_x1, current_y1, current_x2, current_y2 = 0, 0, w, h

    for crop in crops:
        x1, y1, x2, y2 = crop
        width = (current_x2 - current_x1)
        height = (current_y2 - current_y1)

        current_x1 = current_x1 + (x1 * width)
        current_y1 = current_y1 + (y1 * height)
        current_x2 = current_x1 + ((x2 - x1) * width)
        current_y2 = current_y1 + ((y2 - y1) * height)

    return [current_x1, current_y1, current_x2, current_y2]


def non_rectangular_crop(img, points):
    """
    根据提供的四个坐标点对图像进行非矩形裁剪，并返回裁剪区域的归一化xyxy坐标。

    参数:
    image_path (str): 图像文件的路径。
    points (list of tuples): 源图像上的四个坐标点，每个元素是一个二元组(x, y)。
    返回:
    cropped_image (numpy.ndarray): 截取后的图像。
    normalized_coords (tuple): 归一化的xyxy坐标。
    """
    # 读取图像
    # img = cv2.imread(image_path)
    height, width = img.shape[:2]
    points = [(int(p[0] * width), int(p[1] * height)) for p in points]

    # 创建与图像大小相同的黑色掩膜
    mask = np.zeros_like(img)
    # 使用提供的点创建掩膜上的白色多边形
    cv2.fillConvexPoly(mask, np.int32([points]), (255, 255, 255))
    # 使用掩膜与原图像进行位运算
    cropped_image = cv2.bitwise_and(img, mask)
    # 转换掩膜为单通道灰度图像
    gray_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    # 找到掩膜上的非零元素的边界
    coords = cv2.findNonZero(gray_mask)
    # 使用边界来裁剪图像
    x, y, w, h = cv2.boundingRect(coords)
    cropped_image = cropped_image[y:y + h, x:x + w]

    # 计算归一化的xyxy坐标
    xmin, ymin, xmax, ymax = x / width, y / height, (x + w) / width, (y + h) / height
    normalized_coords = (xmin, ymin, xmax, ymax)

    return cropped_image, normalized_coords


def normalize_to_pixel_bounding_box(points, width, height):
    """
    将归一化的边界框坐标转换为像素坐标。

    参数:
        x1_norm (float): 左上角的归一化x坐标。
        y1_norm (float): 左上角的归一化y坐标。
        x2_norm (float): 右下角的归一化x坐标。
        y2_norm (float): 右下角的归一化y坐标。
        width (int): 图像的宽度。
        height (int): 图像的高度。

    返回:
        tuple: 包含整数像素坐标的元组 (x1_pixel, y1_pixel, x2_pixel, y2_pixel)。
    """
    x1_norm, y1_norm, x2_norm, y2_norm = points
    x1_pixel = int(x1_norm * width)
    y1_pixel = int(y1_norm * height)
    x2_pixel = int(x2_norm * width)
    y2_pixel = int(y2_norm * height)

    return x1_pixel, y1_pixel, x2_pixel, y2_pixel


def crop_rectangle_from_image(image, points):
    # 强转坐标参数为整数类型
    height, width = image.shape[:2]
    x1, y1, x2, y2 = normalize_to_pixel_bounding_box(points, width, height)
    # 截取矩形区域
    cropped_image = image[int(y1):int(y2), int(x1):int(x2)]
    return cropped_image

def draw_boxes_on_image_pose(image_path, boxes_dict, confidence_threshold, save_path, resize):
    """
    Draw bounding boxes on an image based on given coordinates and confidence levels.

    Parameters:
    - image_path: Path to the image file.
    - boxes_dict: Dictionary where keys are confidence scores and values are tuples of (x1, y1, x2, y2).
    - confidence_threshold: Minimum confidence level required to draw a box.
    - save_path: Optional path to save the resulting image. If None, the image will be displayed instead.
    """
    Draw = False
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Image not found or unable to load.")
        return

    # Calculate line width based on image size for better visibility
    img_height, img_width = image.shape[:2]
    line_thickness = max(1, min(img_height, img_width) // 400)
    font_scale = max(0.5, min(img_height, img_width) / 800)

    # Iterate over each key-value pair in the dictionary
    for conf, coords in boxes_dict.items():
        # Only proceed if the confidence is above the threshold
        if conf >= confidence_threshold:
            # Unpack the coordinates
            x1, y1, x2, y2 = map(int, coords)
            # Draw the rectangle on the image
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), line_thickness)
            # Add the confidence score as text near the rectangle
            cv2.putText(image, f"Conf: {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 0),
                        line_thickness)
            Draw = True
    # Save or display the image
    if save_path:
        if Draw:
            predix = int(time.time_ns())
            thepath = os.path.dirname(image_path).split("\\")[-1]
            create_directory(f"{save_path}\\{thepath}")
            print(f'{save_path}\\{thepath}\\{predix}.jpg')
            cv2.imwrite(f'{save_path}\\{thepath}\\{predix}.jpg', image)
    else:
        if Draw:
            if resize is not None:
                image = adaptive_resize(image, resize)
            cv2.imshow('Image with Boxes', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


def process_image_for_pose_estimation(imgpath, model_pose, model_pussy, filter, iou):
    # 读取图片
    image = cv2.imread(imgpath)
    # 获取图片的高度和宽度
    height, width = image.shape[:2]
    # 使用姿态检测模型预测图片
    results = model_pose.predict(imgpath, verbose=True, save=False, iou=iou)

    # 创建一个字典来存储姿态估计结果
    pose_dict = {}

    # 遍历所有检测到的对象
    for result in results:
        # 遍历对象的边界框和关键点
        for box, keypoints in zip(result.boxes, result.keypoints.xyn):
            # 检查对象类别是否为人
            if result.names[int(box.cls)] == "person":
                # 裁剪人物区域
                crop1 = box.xyxyn[0].tolist()
                frame_person = crop_rectangle_from_image(image, crop1)
                # 对裁剪出的人物区域进行第一次处理
                dic2 = img_operate_test_pose(frame_person, model_pussy, 0, 0.5)
                # 解析处理结果
                conf2, *crop2 = dic2
                # 计算最终裁剪坐标
                points1 = calculate_final_cropped_coordinates(width, height, crop1, crop2)
                # 根据关键点进行非矩形裁剪
                zitai = keypoints.tolist()
                theframe, xyxy = non_rectangular_crop(image, [zitai[11], zitai[12], zitai[14], zitai[13]])
                # 对非矩形裁剪出的区域进行处理
                dic3 = img_operate_test_pose(theframe, model_pussy, 0, 0.5)
                # 解析处理结果
                conf3, *crop3 = dic3
                # 计算最终裁剪坐标
                points2 = calculate_final_cropped_coordinates(width, height, xyxy, crop3)
                if filter:
                    # 只保留置信度较高的姿态估计
                    if conf2 >= conf3:
                        pose_dict[conf2] = points1
                    else:
                        pose_dict[conf3] = points2
                else:
                    pose_dict[conf2] = points1
                    pose_dict[conf3] = points2
    # 返回姿态估计字典
    return pose_dict
