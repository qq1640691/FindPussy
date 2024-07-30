import os
import random
import shutil


def split_coco_dataset(original_image_path, original_label_path, target_image_base, target_label_base,
                       ratio=(0.8, 0.2)):
    # 创建目标目录
    for dir_name in ['train', 'val']:
        os.makedirs(os.path.join(target_image_base, dir_name), exist_ok=True)
        os.makedirs(os.path.join(target_label_base, dir_name), exist_ok=True)

    # 获取所有图片和标签文件
    image_files = [f for f in os.listdir(original_image_path) if os.path.isfile(os.path.join(original_image_path, f))]
    label_files = [f for f in os.listdir(original_label_path) if os.path.isfile(os.path.join(original_label_path, f))]

    assert len(image_files) == len(label_files), "Number of image files does not match number of label files."

    # 配对图片和标签文件
    file_pairs = list(zip(image_files, label_files))
    random.shuffle(file_pairs)

    # 计算分割点
    total_files = len(file_pairs)
    train_split = int(ratio[0] * total_files)
    train_split + int(ratio[1] * total_files)

    # 划分数据集
    train_pairs = file_pairs[:train_split]
    val_pairs = file_pairs[train_split:]

    # 移动文件
    def copy_files(pairs, target_dir):
        for img_file, label_file in pairs:
            shutil.copy(os.path.join(original_image_path, img_file),
                        os.path.join(target_image_base, target_dir, img_file))
            shutil.copy(os.path.join(original_label_path, label_file),
                        os.path.join(target_label_base, target_dir, label_file))

    copy_files(train_pairs, 'train')
    copy_files(val_pairs, 'val')
    print("Dataset split and files moved successfully.")
