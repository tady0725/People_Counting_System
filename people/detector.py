import torch
import numpy as np

from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import non_max_suppression, scale_coords
from utils.torch_utils import select_device

#很显然，DeepSORT中采用了一个简单（运算量不大）的CNN来提取被检测物体（检测框物体中）的外观特征（低维向量表示），
# 在每次（每帧）检测+追踪后，进行一次物体外观特征的提取并保存。
class Detector:

    def __init__(self):
        self.img_size = 640
        self.threshold = 0.3
        self.stride = 1

        #yolo obj detector 權重
        self.weights = './weights/yolov5m.pt'
        # 選擇使GPU && CPU
        self.device = '0' if torch.cuda.is_available() else 'cpu'
        # 直接使用
        self.device = select_device(self.device)
        # 加載全種模型文件
        model = attempt_load(self.weights, map_location=self.device)

        model.to(self.device).eval()
        model.half()

        self.m = model
        #模型能夠檢測的所有類別標籤
        self.names = model.module.names if hasattr(
            model, 'module') else model.names

    def preprocess(self, img):
        # 對原圖拷貝
        img0 = img.copy()
        # letter_box中做边缘填充 [1080 * 1920 *3] -> [384 * 640 * 3 ] 
        img = letterbox(img, new_shape=self.img_size)[0]
        # [384 * 640 * 3 ] ->  [1080 * 1920 *3]
        # Convert
        # BGR to RGB,
        img = img[:, :, ::-1].transpose(2, 0, 1)
        # 返回一个连续的array，其内存是连续的
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(self.device)
        # 使用到半精度
        img = img.half()
        # 像素
        img /= 255.0
        # 沒有batch size最前面加一個軸
        # [3,384,640] -> [1,3,384,640]

        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        return img0, img

    def detect(self, im):
        # 圖像預處理，返回原圖img0 
        im0, img = self.preprocess(im)
        # 進行預測
        pred = self.m(img, augment=False)[0]
        pred = pred.float()
        pred = non_max_suppression(pred, self.threshold, 0.4)
        # 返回結果
        boxes = []
        for det in pred:

            if det is not None and len(det):
                # 調整檢測框座標。基於預處理後640*640的圖像
                det[:, :4] = scale_coords(
                    img.shape[2:], det[:, :4], im0.shape).round()

                for *x, conf, cls_id in det:
                    lbl = self.names[int(cls_id)]
                    # 篩選出我們要的檢測類別
                    if lbl not in ['person', 'bicycle', 'car', 'motorcycle', 'bus', 'truck']:
                        continue
                    pass
                    x1, y1 = int(x[0]), int(x[1])
                    x2, y2 = int(x[2]), int(x[3])
                    # 檢測框座標(左上右下)，類別標籤
                    
                    boxes.append(
                        (x1, y1, x2, y2, lbl, conf))
        # 返回原圖 
        return boxes
