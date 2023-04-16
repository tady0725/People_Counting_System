# win10版本 yolov5 deepsort 行人 車輛 跟踪 檢測 計數

## 應B站上同學們要求在 win10 運行

- 更新到 python 3.9.10，請不要安裝更高版本。
- 更新到 yolov5 v6.1版。使用的權重文件可以在此下載：https://github.com/ultralytics/yolov5/releases/tag/v6.1
- 更新到 CUDA 11.3+
- 建議保留 Arial.ttf 文件，或在首次運行時由 yolov5 自動下載。


## 功能
- 實現了 出/入 分別計數。
- 顯示檢測類別。
- 默認是 南/北 方向檢測，若要檢測不同位置和方向，可在 main.py 文件第13行和21行，修改2個polygon的點。
- 默認檢測類別：行人、自行車、小汽車、摩托車、公交車、卡車。
- 檢測類別可在 detector.py 文件第60行修改。


### 視頻

bilibili

[![bilibili](https://raw.githubusercontent.com/dyh/win10_yolov5_deepsort_counting/main/cover.png)](https://www.bilibili.com/video/BV13Z4y1C7Dt/ "bilibili")


## 運行環境

- python 3.9.10，pip 22.0.3+
- pytorch 1.10.2+
- pip3 install -r requirements.txt


## 如何運行

0. 確保正確安裝 python 和 CUDA

    ```
    D:\> python -V
   
    D:\> nvidia-smi
   
    D:\> nvcc -V
    ```

1. 下載代碼

    ```
    D:\> git clone https://github.com/dyh/win10_yolov5_deepsort_counting.git
    ```
   
   > 因此repo包含weights和mp4文件，若 git clone 速度慢，可直接下載zip文件：https://github.com/dyh/win10_yolov5_deepsort_counting/archive/refs/heads/main.zip
   
2. 進入目錄

    ```
    D:\> cd win10_yolov5_deepsort_counting
    ```

3. 創建 python 虛擬環境

    ```
    D:\win10_yolov5_deepsort_counting> python -m venv venv
    ```

4. 激活虛擬環境

    ```
     D:\win10_yolov5_deepsort_counting> venv\Scripts\activate
    ```
   
5. 升級pip

    ```
     (venv) D:\win10_yolov5_deepsort_counting> python -m pip install --upgrade pip
    ```

6. 安裝pytorch
   
    > 根據你的操作系統、虛擬環境以及CUDA版本，在 https://pytorch.org/get-started/locally/ 找到對應的安裝命令。我的環境是 win10、pip、CUDA 11.6。
   
    ```
     (venv) D:\win10_yolov5_deepsort_counting> pip3 install torch==1.10.2+cu113 torchvision==0.11.3+cu113 torchaudio===0.10.2+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html
    ```
   
7. 安裝軟件包
   
    ```
     (venv) D:\win10_yolov5_deepsort_counting> pip3 install -r requirements.txt
    ```
   
8. 在 main.py 文件中第66行，設置要檢測的視頻文件路徑，默認為 './video/test.mp4'
   
    > 140MB的測試視頻可以在這裡下載：https://pan.baidu.com/s/1qHNGGpX1QD6zHyNTqWvg1w 提取碼: 8ufq 
   
    ```
    capture = cv2.VideoCapture(r'video\test.mp4')
    ```
   
9. 運行程序

    ```
    (venv) D:\win10_yolov5_deepsort_counting> python main.py
    ```


## 使用框架

- https://github.com/Sharpiless/Yolov5-deepsort-inference
- https://github.com/ultralytics/yolov5/
- https://github.com/ZQPei/deep_sort_pytorch