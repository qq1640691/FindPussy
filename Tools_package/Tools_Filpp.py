import os
from concurrent.futures import ThreadPoolExecutor

import cv2
import numpy as np


def process_image_and_annotation(img_file, image_dir, annotation_dir):
    img_path = os.path.join(image_dir, img_file)
    img_file_lower = img_file.lower()

    with open(img_path, 'rb') as f:
        img = cv2.imdecode(np.frombuffer(f.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    flipped_img = cv2.flip(img, 1)

    # 添加前缀并保存在原目录
    output_img_file = f"flipped_{img_file}"
    output_img_path = os.path.join(image_dir, output_img_file)
    cv2.imwrite(output_img_path, flipped_img)

    base_name, _ = os.path.splitext(img_file)
    for ext_lower in ['.jpg', '.jpeg', '.png']:
        if img_file_lower.endswith(ext_lower):
            break
    anno_file = f"{base_name}.txt"
    anno_path = os.path.join(annotation_dir, anno_file.lower())

    if os.path.exists(anno_path):
        with open(anno_path, 'r') as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            class_id, x_center, y_center, width, height = map(float, line.strip().split())
            x_center = 1 - x_center

            new_line = f"{class_id} {x_center} {y_center} {width} {height}\n"
            new_lines.append(new_line)

        # 添加前缀并保存在原目录
        output_anno_file = f"flipped_{anno_file}"
        output_anno_path = os.path.join(annotation_dir, output_anno_file)
        with open(output_anno_path, 'w') as f:
            f.writelines(new_lines)
    else:
        print(f"Warning: Annotation file not found for {img_file}")


def flip_images_and_annotations(image_dir, annotation_dir):
    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(annotation_dir, exist_ok=True)

    image_extensions = ['.jpg', '.jpeg', '.png']

    files_to_process = [img_file for img_file in os.listdir(image_dir) if
                        any(img_file.lower().endswith(ext) for ext in image_extensions)]

    with ThreadPoolExecutor() as executor:
        executor.map(
            lambda img_file: process_image_and_annotation(img_file, image_dir, annotation_dir), files_to_process)
