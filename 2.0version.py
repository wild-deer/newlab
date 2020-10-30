import sys
import cv2
import time
from PyQt5 import QtCore
from PyQt5.QtCore import QThread  # 引入线程
from PyQt5.QtGui import QImage, QPixmap, QColor

from Algorithm.toyDetect import NLToyDetect  # 引入算法sdk类
from PyQt5.QtWidgets import QMainWindow, QApplication
from TL_UI import Ui_MainWindow
import tct_trans


# 增加对非汽车的过滤

class CameraThread(QThread):  # 摄像头线程类
    # 摄像头采集图片
    updatedM = QtCore.pyqtSignal(int)  # 发射信号

    def __init__(self, mw):
        self.mw = mw  # UI界面的对象
        self.working = True
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        while self.working:
            QApplication.processEvents()  # 将处理所有事件队列中的事件并返回给调用者:application
            if not self.mw.CapIsbasy:  # 初值为false
                # 采集图像的过程中
                self.mw.CapIsbasy = True
                # 调用UI界面的摄像头对象，获取图片
                ret, image = self.mw.cap.read()  # 获取新的一帧图片
                time.sleep(1/30)
                if not ret:  # 如果ret不为0意味着获取图片失败
                    print("Capture Image Failed")
                    self.mw.CapIsbasy = False
                    continue
                img_len = len(image.shape)  # 图像的维度是shape，图像的第一维度大小是len
                if img_len == 3:
                    self.mw.limg = image  # 将获取的图片赋给UI界面变量limg
                else:
                    self.mw.limg = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)  # 颜色空间转换
                self.mw.CapIsbasy = False
                self.updatedM.emit(self.mw.frameID)  # 触发当前事件附加参数都会传给监听器回调

            else:
                time.sleep(1.0 / 50)  # 间隔时间 再开始获取图片

    def stop(self):
        if self.working:
            self.working = False
            print('摄像头采集线程退出')

class LedThread(QThread):#红绿灯线程类
    updatedcar = QtCore.pyqtSignal(int)  # 定义一个信号

    def __init__(self, mw):
        self.mw = mw  # 传入UI界面对象
        self.working = True
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        while self.working:
            pass
            # print(str(self.mw.car1))
    def stop(self):
        if self.working:
            self.working = False
            print('ToyDetectThread线程退出了')


class tcp_trans(QThread):  # 红绿灯线程类
    updatedcar = QtCore.pyqtSignal(int)  # 定义一个信号

    def __init__(self, mw):
        self.mw = mw  # 传入UI界面对象
        self.working = True
        QThread.__init__(self)


    def __del__(self):
        self.wait()

    def run(self):
        while self.working:
            tct_trans.send_carNumber(self.mw.tcp_client,self.mw.car1)
            time.sleep(1)
            print(str(self.mw.car1))

    def stop(self):
        if self.working:
            self.working = False
            print('ToyDetectThread线程退出了')


class ToyDetectThread(QThread):
    # 物品目标检测算法sdk调用线程
    updatedImage = QtCore.pyqtSignal(int)  # 定义一个信号
    updatedcar = QtCore.pyqtSignal(int)  # 定义一个信号
    def __init__(self, mw):
        self.mw = mw  # 传入UI界面对象
        self.working = True
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        while self.working:
            if self.mw.AlgIsbasy == False and not (self.mw.limg is None):  # 表示成功获取图片
                self.mw.AlgIsbasy = True  # 开始处理图片
                limg = self.mw.limg  # 图片赋值
                ret = self.mw.TL.NL_TD_InitVarIn(limg)  # 调用算法进行处理检测
                if ret == 0:
                    ret = self.mw.TL.NL_TD_Process_C()  # 调用算法sdk的主处理函数  返回值是目标个数
                    height, width, bytesPerComponent = limg.shape  # 照片的三维   像素
                    bytesPerLine = bytesPerComponent * width  # 图像每行锁占用的字节数
                    rgb = cv2.cvtColor(limg, cv2.COLOR_BGR2RGB)  # 颜色空间转换
                    if ret > 0:
                        # 输出结果
                        for i in range(self.mw.TL.djTDVarOut.dwObjectSize):
                            outObject = self.mw.TL.djTDVarOut.pdjToyInfors[i]

                            # outObject是 Algorithm.toyDetect.Struct_TD_ObjInfor 类型变量

                            # print(type(outObject))
                            # print(outObject.className == "car")


                            if str(outObject.className, "utf-8").replace('\r', '') == "car":
                                self.mw.car_number_1.setText(str(ret))
                                self.mw.car1 = ret
                                font = cv2.FONT_HERSHEY_SIMPLEX  # 定义字体
                                # 在图片上，标识类别名称
                                imgzi = cv2.putText(rgb, str(outObject.className, "utf-8").replace('\r', ''),
                                                    (int(outObject.dwLeft) + 2, int(outObject.dwBottom) - 2), font,
                                                    1.4, (255, 0, 0), 2)

                                """
                                   putText(img, text, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]]) -> img
                                   .   @brief Draws a text string.
                                   .   
                                   .   The function cv::putText renders the specified text string in the image. Symbols that cannot be rendered
                                   .   using the specified font are replaced by question marks. See #getTextSize for a text rendering code
                                   .   example.
                                   .   
                                   .   @param img Image.
                                   .   @param text Text string to be drawn.
                                   .   @param org Bottom-left corner of the text string in the image.
                                   .   @param fontFace Font type, see #HersheyFonts.
                                   .   @param fontScale Font scale factor that is multiplied by the font-specific base size.
                                   .   @param color Text color.
                                   .   @param thickness Thickness of the lines used to draw a text.
                                   .   @param lineType Line type. See #LineTypes
                                   .   @param bottomLeftOrigin When true, the image data origin is at the bottom-left corner. Otherwise,
                                   .   it is at the top-left corner.
                                   """
                                # 画出物体框
                                cv2.rectangle(rgb, (int(outObject.dwLeft), int(outObject.dwTop)),
                                              (int(outObject.dwRight), int(outObject.dwBottom)), (0, 0, 255), 2)
                                # print('类别名：' + str(outObject.className, "utf-8").replace('\r', '') + '  置信度: ' + str(
                                #     outObject.fscore))  # 打印结果在命令行

                                """
                                    rectangle(img, pt1, pt2, color[, thickness[, lineType[, shift]]]) -> img
                                    .   @brief Draws a simple, thick, or filled up-right rectangle.
                                    .   
                                    .   The function cv::rectangle draws a rectangle outline or a filled rectangle whose two opposite corners
                                    .   are pt1 and pt2.
                                    .   
                                    .   @param img Image.
                                    .   @param pt1 Vertex of the rectangle.
                                    .   @param pt2 Vertex of the rectangle opposite to pt1 .
                                    .   @param color Rectangle color or brightness (grayscale image).
                                    .   @param thickness Thickness of lines that make up the rectangle. Negative values, like #FILLED,
                                    .   mean that the function has to draw a filled rectangle.
                                    .   @param lineType Type of the line. See #LineTypes
                                    .   @param shift Number of fractional bits in the point coordinates.



                                    rectangle(img, rec, color[, thickness[, lineType[, shift]]]) -> img
                                    .   @overload
                                    .   
                                    .   use `rec` parameter as alternative specification of the drawn rectangle: `r.tl() and
                                    .   r.br()-Point(1,1)` are opposite corners
                                    """

                    showImage = QImage(rgb.data, width, height, bytesPerLine, QImage.Format_RGB888)  # 将处理过的图片保存用于显示
                    self.mw.showImage = QPixmap.fromImage(showImage)

                    self.updatedImage.emit(self.mw.frameID)  # 触发信号，去执行UI界面的相关函数
                    self.updatedcar.emit(ret)
                else:
                    print('Error code1:', ret)
                    time.sleep(100)
                self.mw.AlgIsbasy = False
            else:
                time.sleep(0.001)

    def stop(self):  # 重写stop方法
        if self.working:
            self.working = False
            print('ToyDetectThread线程退出了')





class TL_Page(QMainWindow, Ui_MainWindow):  # 窗口页面
    def __init__(self):  # 初始化界面函数
        super(TL_Page, self).__init__()  # 继承UI
        self.setupUi(self)

        # 设置线程参数,在线程中会用到所以提前 定义
        self.AlgIsbasy = False
        self.CapIsbasy = False
        self.frameID = 0
        self.car1 = 0  #路口一的车辆数保存在这里
        self.car2 = 0

        # 初始红绿灯参数
        # self.red_time.setText(str(QColor('red')))
        # self.red_time.setStyleSheet("background-color: red")
        # self.yellow_time.setText("     2s")
        # self.green_time.setText("     10s")

        self.car_number_1.setText("0")


        # 设置摄像头视频采集参数
        self.cap = cv2.VideoCapture("2.avi")  # 0是笔记本自带摄像头，可参数：“视频路径”
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # 设置分辨率
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.limg = None  # 将摄像头线程采集的一帧图片保存在这里
        self.showImage = None  # 将经过处理的图片保存在这里


        # tcp传输类
        self.tcp_client = tct_trans.init_tcp()


        # 调用算法类-------实例化算法sdk类，并初始化加载模型和配值
        self.configPath = configPath  # 模型防止路径信息
        self.libNamePath = libNamePath  # 算法sdk的so库
        self.TL = NLToyDetect(self.libNamePath)  # 实例化算法sdk类对象NLToyDetect
        ret = self.TL.NL_TD_ComInit(self.configPath, dwClassNum, dqThreshold, pbyModel, pbyLabel)  # 实例化对象调用sdk里的算法加载初始化
        if ret != 0:
            print('Error code:', ret)

        self.start_btn.clicked.connect(self.start_btn_func)  # 开始按钮，通过点击触发函数
        self.stop_btn.clicked.connect(self.stop_btn_func)  # 停止按钮，通过点击触发函数
    def setCarnumber(self):
        self.car_number_1.setText(str(self.car1))
    def showframe(self):
        # 显示视频流
        self.label_show_camera.setPixmap(self.showImage)

    def start_btn_func(self):
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

        # 线程1相机采集
        self.camera_th = CameraThread(self)
        # self.camera_th.updatedM.connect(self.showframe)              #调用线程 并启用线程
        self.camera_th.start()

        # 线程2算法处理
        self.toy_detect_th = ToyDetectThread(self)
        self.toy_detect_th.updatedImage.connect(self.showframe)  # 将线程信号绑定在显示函数上
        self.toy_detect_th.updatedcar.connect(self.setCarnumber)  # 将线程信号绑定在显示函数上
        self.toy_detect_th.start()
        #线程3红绿灯处理
        self.led_th = LedThread(self)
        self.led_th.start()
        #tcp线程处理
        self.tcp_trans_th = tcp_trans(self)
        self.tcp_trans_th.start()
    def stop_btn_func(self):
        self.stop_btn.setEnabled(False)
        self.start_btn.setEnabled(True)
        try:
            self.camera_th.stop()
            self.camera_th.quit()
            self.toy_detect_th.stop()
            self.toy_detect_th.quit()
            del self.camera_th
            del self.toy_detect_th
        except Exception as e:
            pass


# 启动主程序
if __name__ == '__main__':
    # 算法配值参数
    configPath = b"/system/3559v100_AI_model/config/Detect_config.ini"  # 算法配置文件参数
    libNamePath = '/system/3559v100_AI_libs/libNL_DetectYoloEnc.so'  # 算法sdk的so库
    dwClassNum = 13  # 类别数
    dqThreshold = 0.78  # 置信度阈值
    pbyModel = b"/system/3559v100_AI_model/model/ObjDetect/NL_ToyDetect_V3.2.wk"  # 算法模型路径
    pbyLabel = b"/system/3559v100_AI_model/model/ObjDetect/td_v3.2.txt"  # 算法模型label文件路径
    app = QApplication(sys.argv)
    tl_page = TL_Page()
    tl_page.show()

    sys.exit(app.exec_())

# 调用笔记本自带摄像头
'''cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    cv2.imshow("Video", frame)
    # 读取内容
    if cv2.waitKey(10) == ord("q"):
        break

# 随时准备按q退出
cap.release()
cv2.destroyAllWindows()'''
