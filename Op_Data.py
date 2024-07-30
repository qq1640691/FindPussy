import os

from Tools_package.Tools_DataClean import move_files_and_delete_dirs, process_media_files
from Tools_package.Tools_DelDup import delete_original_images, delete_original_and_corresponding_txt
from Tools_package.Tools_Filpp import flip_images_and_annotations
from Tools_package.Tools_ShowPic import display_images_with_boxes
from Tools_package.Tools_huafendata import split_coco_dataset
from Tools_package.Tools_rename import rename_file_pairs, rename_files
from Tools_package.Tools_xmltotxt import process_all_xmls_in_folder

'''
    数据集处理相关,在训练时对数据进行处理
    这段代码主要包含了四个部分的功能：
    第1个部分是处理数据集的准备工作。首先通过调用move_files_and_delete_dirs函数将数据集中的所有文件移动到父目录下，并重命名以避免重名。
        然后可以选择性地调用rename_files_in_directory函数对文件进行重命名，或者调用process_media_files函数将视频文件移动到指定文件夹，并删除其他类型的文件。
        最后，可以选择性地调用delete_original_images函数删除原始图片文件。
    第2个部分是处理数据集的扩充和格式转换。先把xm转为txt,然后通过调用flip_images_and_annotations函数将所有的图片水平翻转以扩充数据集，
        并保存到原文件夹中，同时修改对应的标注文件。最后通过调用rename_file_pairs函数对图片和标注文件进行重命名，确保随机性。
    第3个部分是通过调用split_coco_dataset函数将数据集划分为COCO128格式的数据集，训练集和验证集的比例为8:2。
    第4个部分是测试数据集的合规性。通过调用display_images_with_boxes函数显示带有标注框的图片，可以使用快捷键AD进行上一张和下一张的切换，以检查转换后的COCO128格式的数据集是否合规。
'''


def main_switch(operation_num):
    operations = {
        1: "prepare_data",
        2: "augment_data",
        3: "split_dataset",
        4: "test_results"
    }
    '''
        给出图片的文件夹即可,自己给,这个一定要看,注意
    '''
    image_directory = r"D:\迅雷下载"
    if not os.path.exists(image_directory):
        print(f"文件夹 {image_directory} 不存在.")
        return
    if operation_num in operations:
        operation = operations[operation_num]
        print(f"开始执行操作：{operation}...")

        if operation == 'prepare_data':
            for filename in os.listdir(image_directory):
                # print(f"正在处理文件：{filename}")
                # print(os.path.join(image_directory, filename))
                move_files_and_delete_dirs(os.path.join(image_directory, filename))
            # 可选操作：重命名文件,如果文件已经是全英文/数字不需要重命名
            # rename_files(image_directory)
            # 可选操作：处理媒体文件,移动所有视频文件到另一个目录
            # dest_directory = "自己指定一下"
            # process_media_files(image_directory , dest_directory)
            # 可选操作：删除图片文件(删除所有相同文件,md5相同的)
            # delete_original_images(image_directory)
            print("数据准备完成！")

        elif operation == 'augment_data':
            text_directory = f"{image_directory}\\outputs"
            process_all_xmls_in_folder(text_directory)
            flip_images_and_annotations(image_dir=image_directory, annotation_dir=text_directory)
            rename_file_pairs(image_directory, text_directory)
            # 可选操作,剔除md5相同的文件(在数据集标注之后,二选一)
            # delete_original_and_corresponding_txt(image_directory, text_directory)
            print("数据增强完成！")

        elif operation == 'split_dataset':
            text_directory = f"{image_directory}\\outputs"
            split_coco_dataset(original_image_path=image_directory, original_label_path=text_directory,
                               target_image_base="datasets\\pussy\\images", target_label_base="datasets\\pussy\\labels")
            print("数据集划分完成！")

        elif operation == 'test_results':
            image_directory = "datasets/pussy/images/train"
            text_directory = "datasets/pussy/labels/train"
            display_images_with_boxes(image_directory, text_directory)
            print("测试完成！")

    else:
        print("无效的操作选项！")


# 选择功能
if __name__ == '__main__':
    operation_num = int(input(
        "请输入你想要执行的操作编号\n1-准备数据(不执行1别执行其他的,在打标之前执行,其他的在打标之后执行)，\n2-数据增强\n3-划分数据集为coco格式\n4-测试结果:\n"))
    main_switch(operation_num)
