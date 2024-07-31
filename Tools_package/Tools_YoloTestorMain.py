import os

from Tools_package.Tools_VI_Operate import img_operate, video_operate
from Tools_package.Tools_VI_Test import img_operate_test, video_operate_test


def is_media_file(filepath):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff']
    video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv', '.webm', '.mpeg', '.mpg']

    if any(filepath.endswith(ext) for ext in image_extensions):
        return 'image'
    elif any(filepath.endswith(ext) for ext in video_extensions):
        return 'video'
    else:
        return None


'''想看视频取消注释'''


def yolo_test(data_path, model, confidence, iou, resize):
    for root, dirs, files in os.walk(data_path):
        for file in files:
            filepath = os.path.join(root, file)
            media_type = is_media_file(filepath)

            if media_type == 'image':
                img_operate_test(filepath, model, confidence, iou, resize)
            elif media_type == 'video':
                # video_operate_test(filepath, model, confidence, iou, resize)
                pass


'''不处理视频,每帧都取有点麻烦'''


def yolo_main(data_path, model, save_path_img, save_path_video, confidence, iou):
    for root, dirs, files in os.walk(data_path):
        for file in files:
            filepath = os.path.join(root, file)
            media_type = is_media_file(filepath)

            if media_type == 'image':
                img_operate(filepath, model, save_path_img, confidence, iou)
            elif media_type == 'video':
                # video_operate(filepath, model, save_path_video, confidence, iou)
                pass
