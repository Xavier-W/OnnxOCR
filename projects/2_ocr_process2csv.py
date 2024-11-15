import sys
sys.path.append('./')
from projects.utils import OCR_Project

if __name__ == "__main__":
    img_root_dir = "/home/maoyc/OnnxOCR/projects"
    boxes_txt = './20241114-160651.txt'
    csv_path = "./20241114-160651.csv"
    
    ocr = OCR_Project(img_root_dir, boxes_txt)

    content = []
    for img_path in ocr.img_path_list:
        results = ocr.process(img_path)
        # print("total time: {:.3f}".format(e - s))
        print("result:", results)
        # cv2.imshow('cropped', cropped)
        # if cv2.waitKey(0) == 27:
        #     break
        content.append(results)
    ocr.to_csv(csv_path, content)
    
        
        
