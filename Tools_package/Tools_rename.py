import os
import random
import string


def generate_random_string(length=10):
    """生成指定长度的随机字符串"""
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))


def rename_file_pairs(directory_img, directory_txt):
    """重命名目录下的所有图片和txt文件对，确保没有重复的文件名"""
    file_dict = {}
    for filename in os.listdir(directory_img):
        if os.path.isfile(os.path.join(directory_img, filename)) and filename.lower().endswith(
                ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            base_name, ext = os.path.splitext(filename)
            txt_filename = base_name + '.txt'
            if os.path.isfile(os.path.join(directory_txt, txt_filename)):
                new_filename = generate_random_string()
                while new_filename in file_dict.values():
                    new_filename = generate_random_string()
                file_dict[filename] = new_filename
                os.rename(os.path.join(directory_img, filename),
                          os.path.join(directory_img, new_filename + ext))
                os.rename(os.path.join(directory_txt, txt_filename),
                          os.path.join(directory_txt, new_filename + '.txt'))


def rename_files(directory):
    """重命名目录下的所有图片，确保没有重复的文件名"""
    file_dict = {}
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)) and filename.lower().endswith(
                ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            new_filename = generate_random_string()
            while new_filename in file_dict.values():
                new_filename = generate_random_string()
            file_dict[filename] = new_filename
            os.rename(os.path.join(directory, filename),
                      os.path.join(directory, new_filename + os.path.splitext(filename)[1]))
