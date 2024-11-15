import xml.etree.ElementTree as ET

# XML文件路径
xml_file_path = './20241114-160651.xml'
# TXT文件路径
txt_file_path = './20241114-160651.txt'

# 解析XML文件
tree = ET.parse(xml_file_path)
root = tree.getroot()

# 打开TXT文件准备写入
with open(txt_file_path, 'w') as file:
    # 遍历所有的object元素
    for obj in root.findall('object'):
        bndbox = obj.find('bndbox')
        xmin = bndbox.find('xmin').text
        ymin = bndbox.find('ymin').text
        xmax = bndbox.find('xmax').text
        ymax = bndbox.find('ymax').text

        # 写入TXT文件
        file.write(f'{xmin} {ymin} {xmax} {ymax}\n')

print(f'Bounding box information has been written to {txt_file_path}')