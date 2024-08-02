import os

from Tools_package.Tools_Pose import process_image_for_pose_estimation, draw_boxes_on_image_pose
from Tools_package.Tools_VI_Operate import video_operate
from Tools_package.Tools_VI_Test import video_operate_test


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


def yolo_test(data_path, model_pose, model_pussy, save_path_img, confidence, iou, resize,filter):
    for root, dirs, files in os.walk(data_path):
        for file in files:
            filepath = os.path.join(root, file)
            media_type = is_media_file(filepath)

            if media_type == 'image':
                # print(filepath)
                dic = process_image_for_pose_estimation(filepath, model_pose, model_pussy, filter=filter, iou=iou)
                draw_boxes_on_image_pose(filepath, dic, confidence, save_path_img, resize)
            elif media_type == 'video':
                # video_operate_test(filepath, model_pussy, confidence, iou, resize)
                pass


'''不处理视频,每帧都取有点麻烦'''

'''reszie=None,则保存路径必须有'''
def yolo_main(data_path, model_pose, model_pussy, save_path_img, save_path_video, confidence, iou,resize=None):
    for root, dirs, files in os.walk(data_path):
        for file in files:
            filepath = os.path.join(root, file)
            media_type = is_media_file(filepath)

            if media_type == 'image':
                dic = process_image_for_pose_estimation(filepath, model_pose, model_pussy, filter=False, iou=iou)
                draw_boxes_on_image_pose(filepath, dic, confidence, save_path_img, resize)
            elif media_type == 'video':
                # video_operate(filepath, model_pussy, save_path_video, confidence, iou)
                pass
