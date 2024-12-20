import os
import cv2
import csv
import sys
import re
sys.path.append('./')
from onnxocr.onnx_paddleocr import ONNXPaddleOcr

class OCR_Project():
    def __init__(self, img_root_dir, boxes_txt):
        self.model = ONNXPaddleOcr(use_angle_cls=False, use_gpu=True)
        print("----------------reading images----------------")
        self.img_path_list = self.get_images_list(img_root_dir)
        print("----------------reading done----------------")
        self.boxes = self.get_boxes(boxes_txt)
        self.head = ["时间","吊重(kg)","载重比(%)","力矩比(%)","回转(°)","高度(m)","幅度(m)","风速(m/s)","水平角(°)","垂直角(°)","最大载重(kg)","塔身高度(m)","前臂长度(m)","后臂长度(m)","实际吊重(kg)","载重比(%)","回转(°)","小车幅度(m)","吊钩高度(m)","风速(m/s)","垂直角(°)","水平角(°)","倍率","相对坐标X","相对坐标Y","首节高度(m)","塔节高度(m)","节数","塔身高度(m)","塔帽高度(m)","前臂长度(m)","后臂长度(m)","左转限位(°)","右转限位(°)","近限位(m)","远限位(m)","高限位(m)","力矩限位(%)","驾驶员"]


    def get_boxes(self, boxes_txt):
        with open(boxes_txt, 'r') as f:
            boxes = f.readlines()
        box_list = []
        for box in boxes:
            box_list.append([int(i) for i in box.strip().split(' ')])
        return box_list

    def get_images_list(self, src_dir, extensions=('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')):
        image_paths = []
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                if file.lower().endswith(extensions):
                    image_paths.append(os.path.join(root, file))
        image_paths = sorted(image_paths, key=lambda path: os.path.basename(path))
        return image_paths

    def process(self, img_path):
        results = [os.path.splitext(os.path.basename(img_path))[0]]
        cropped_list = self.ori_to_cropped(img_path)
        for i, cropped in enumerate(cropped_list):
            result = self.model.ocr(cropped, det=False, cls=False, rec=True)
            if i<len(cropped_list)-1:
                results.append(self.result_process(result[0][0][0]))
            else:
                results.append(result[0][0][0].replace(" ", ""))
        return results

    def result_process(self, result):
        result = result.replace("。", "0")
        result = result.replace("口", "0")
        result = re.sub(r'[^0-9\.\+\-]', '', result)
        return result
        # result = result.replace("*", "")
        # result = result.replace(" ", "")
        # return result

    def ori_to_cropped(self, img_path):
        img_data = cv2.imread(img_path)
        cropped_list = []
        for box in self.boxes:
            xmin, ymin, xmax, ymax = box
            cropped_list.append(img_data[ymin:ymax+1, xmin:xmax+1, :])
        return cropped_list
    
    def to_csv(self, csv_path, content):
        content.insert(0, self.head)
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for row in content:
                if '' in row:
                    row = [row[0]]+['' for i in row[1:]]
                writer.writerow(row)  # 写入一行数据
