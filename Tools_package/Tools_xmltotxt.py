import os
import xml.etree.ElementTree as Et


def parse_xml(file_path):
    tree = Et.parse(file_path)
    root = tree.getroot()

    # 解析图片尺寸
    size = root.find('size')
    width = float(size.find('width').text)
    height = float(size.find('height').text)

    # 解析标注信息
    objects = root.findall('.//item')
    annotations = []

    for obj in objects:
        name = obj.find('name').text
        bndbox = obj.find('bndbox')

        xmin = float(bndbox.find('xmin').text)
        ymin = float(bndbox.find('ymin').text)
        xmax = float(bndbox.find('xmax').text)
        ymax = float(bndbox.find('ymax').text)

        # 归一化处理
        x_center = (xmin + xmax) / (2 * width)
        y_center = (ymin + ymax) / (2 * height)
        width_norm = (xmax - xmin) / width
        height_norm = (ymax - ymin) / height

        annotations.append((name, x_center, y_center, width_norm, height_norm))

    return annotations


def save_as_yolo_txt(annotations, output_file):
    with open(output_file, 'w') as f:
        for name, x_center, y_center, width, height in annotations:
            # 假设类别名到ID的映射
            class_id = class_name_to_id(name)
            line = f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"
            f.write(line)


def class_name_to_id(class_name):
    # 假设的类别名到ID映射
    class_map = {
        'pussy': 0,
        'Pussy': 0
    }
    return class_map.get(class_name, 0)


def process_all_xmls_in_folder(folder_path):
    no_object_files = []  # 创建一个空列表来存储没有<object>标签的文件名

    # 遍历指定文件夹下的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            file_path = os.path.join(folder_path, filename)

            # 解析XML文件
            tree = Et.parse(file_path)
            root = tree.getroot()

            # 检查是否存在至少一个矩形框标注
            objects = root.findall('.//object')
            if len(objects) > 0:
                # 解析XML文件并获取标注信息
                annotations = parse_xml(file_path)

                # 获取不带扩展名的文件名
                base_name = os.path.splitext(filename)[0]

                # 构建输出文件名，注意这里输出文件的路径与XML文件相同
                output_file_path = os.path.join(folder_path, f'{base_name}.txt')

                # 将标注信息保存为YOLO格式的文本文件
                save_as_yolo_txt(annotations, output_file_path)
            else:
                no_object_files.append(filename)  # 将没有<object>标签的文件名添加到列表中

    # 处理完所有文件后，输出没有<object>标签的文件名
    if no_object_files:
        print("The following files do not contain any object tags and were skipped:")
        for no_obj_file in no_object_files:
            print(no_obj_file)
    else:
        print("All processed files contained at least one object tag.")

        # 删除所有的XML文件
    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            file_path = os.path.join(folder_path, filename)
            os.remove(file_path)
            print(f"Deleted XML file: {file_path}")

    delete_corresponding_images_of_no_objects(folder_path, no_object_files)


def delete_corresponding_images_of_no_objects(folder_path, no_object_files):
    # 返回上一级目录
    parent_dir = os.path.dirname(folder_path)

    # 遍历没有<object>标签的XML文件列表
    for xml_filename in no_object_files:
        # 获取不带扩展名的文件名
        base_name = os.path.splitext(xml_filename)[0]

        # 构建可能的图片文件名
        possible_image_filenames = [f'{base_name}.jpg', f'{base_name}.png', f'{base_name}.jpeg']

        # 在上一级目录中查找并尝试删除这些图片
        for image_filename in possible_image_filenames:
            image_path = os.path.join(parent_dir, image_filename)
            if os.path.exists(image_path):
                os.remove(image_path)
                print(f"Deleted corresponding image: {image_path}")
