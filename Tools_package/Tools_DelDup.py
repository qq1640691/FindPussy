import os
import hashlib


def delete_original_and_corresponding_txt(directory, txt_directory):
    """
    在指定目录下查找重复的图片，删除原始图片及其在txt_directory中的同名TXT文件，
    同时保留重复的图片。
    """
    # 用于存储文件的MD5值和对应的文件路径
    hash_dict = {}
    # 遍历指定目录下的所有文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    # 计算文件的MD5值
                    file_hash = hashlib.md5(f.read()).hexdigest()
                    # 如果MD5值已经存在于字典中，则表示找到了重复的图片
                    if file_hash in hash_dict:
                        # 删除原始图片
                        original_image_path = hash_dict[file_hash]
                        print(original_image_path)
                        os.remove(original_image_path)
                        # 构建对应的TXT文件的路径
                        txt_file = hash_dict[file_hash].split('.')[0] + '.txt'
                        name = txt_file.split('\\')[-1]
                        txt_path = os.path.join(txt_directory, name)
                        print(txt_path)
                        # 删除TXT文件
                        if os.path.exists(txt_path):
                            os.remove(txt_path)
                            pass
                    else:
                        hash_dict[file_hash] = file_path


def delete_original_images(directory):
    """
    在指定目录下查找重复的图片，并删除原始图片，保留重复的图片。
    """
    # 用于存储文件的MD5值和对应的文件路径
    hash_dict = {}
    # 遍历指定目录下的所有文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    # 计算文件的MD5值
                    file_hash = hashlib.md5(f.read()).hexdigest()
                    # 如果MD5值已经存在于字典中，则表示找到了重复的图片
                    if file_hash in hash_dict:
                        # 删除原始图片
                        original_image_path = hash_dict[file_hash]
                        print(original_image_path)
                        os.remove(original_image_path)
                    else:
                        hash_dict[file_hash] = file_path
