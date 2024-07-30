# -*- coding: utf-8 -*-
import os
import shutil
import time


def move_files_and_delete_dirs(root_dir):
    """
    移动所有子目录下的文件到根目录，并删除这些子目录。
    如果有文件名冲突，则使用当前纳秒数重命名文件，同时保留扩展名。
    先移动所有文件，再统一删除目录。
    """

    # 收集所有文件的路径
    all_files = []
    for root, dirs, files in os.walk(root_dir):
        all_files.extend([os.path.join(root, file) for file in files])

    nano_time = None  # 初始化为None，将在需要时生成

    # 处理文件
    moved_files = set()
    for file_path in all_files:
        if file_path not in moved_files:
            base_name, ext = os.path.splitext(os.path.basename(file_path))
            dest_file_path = os.path.join(root_dir, base_name + ext)

            # 检查目标文件是否已存在
            if os.path.exists(dest_file_path):
                # 动态生成时间戳，避免文件名冲突
                nano_time = int(time.time() * 1e9)
                new_file_name = f"{base_name}_{nano_time}{ext}"
                dest_file_path = os.path.join(root_dir, new_file_name)

            # 移动文件到根目录
            shutil.move(file_path, dest_file_path)
            moved_files.add(file_path)  # 添加已移动的文件到集合
    # 删除所有空目录，从底层开始
    for root, dirs, files in os.walk(root_dir, topdown=False):
        if not os.listdir(root):  # 检查目录是否为空
            try:
                os.rmdir(root)
            except OSError:
                # 忽略非空目录的错误，仅删除空目录
                pass


def rename_files_in_directory(directory_path):
    """
    遍历指定目录，对其中的文件按遇到的顺序从0开始重命名，
    新的文件名格式为：[root_directory_name]_[index][extension]。
    以父文件夹的名称重命名
    """
    if not os.path.isdir(directory_path):
        print(f"Directory {directory_path} does not exist.")
        return
    # 获取目录中所有文件的列表
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    # 获取目录名作为前缀
    parent_dir_name = os.path.basename(directory_path)
    # 重命名每个文件
    for index, filename in enumerate(files):
        old_file_path = os.path.join(directory_path, filename)
        base_name, ext = os.path.splitext(filename)
        # 构建新的文件名
        new_filename = f"{parent_dir_name}_{index:04d}{ext}"
        new_file_path = os.path.join(directory_path, new_filename)
        # 重命名文件
        os.rename(old_file_path, new_file_path)
        print(f"Renamed '{filename}' to '{new_filename}'")


def process_media_files(source_folder, video_destination_folder):
    """
    遍历文件夹，删除非图片和视频文件，并将视频文件移动到指定文件夹。

    :param source_folder: 包含原始媒体文件的文件夹路径。
    :param video_destination_folder: 视频文件的目标文件夹路径。
    """
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv']

    # 确保视频目标文件夹存在
    if not os.path.exists(video_destination_folder):
        os.makedirs(video_destination_folder)

    # 遍历文件夹中的所有文件
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)
        # 判断文件是否为图片或视频
        if os.path.isfile(file_path):
            extension = os.path.splitext(filename)[1].lower()
            if extension in image_extensions:
                # 文件是图片，保留
                pass
            elif extension in video_extensions:
                # 文件是视频，移动到视频目标文件夹
                shutil.move(file_path, os.path.join(video_destination_folder, filename))
            else:
                # 文件既不是图片也不是视频，删除
                os.remove(file_path)

    print("处理完成，非图片和视频文件已被删除，视频文件已移动。")
