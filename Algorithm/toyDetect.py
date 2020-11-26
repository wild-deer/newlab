# -*- coding: utf-8 -*-
from ctypes import *
import os

import cv2
import numpy as np


# 结构体定义
class Struct_Handle(Structure):
    _fields_ = [("pvModel", c_void_p), ("pvBuf", c_void_p), ("qwBufLen", c_longlong)]


class Struct_TD_VarIn(Structure):
    _fields_ = [("pubyIm", c_char_p), ("dwWidth", c_int), ("dwHeight", c_int), ("dwChannel", c_int)]


class Struct_TD_ObjInfor(Structure):
    _fields_ = [("dwClassID", c_int), ("dwLeft", c_int), ("dwTop", c_int), ("dwRight", c_int),
                ("dwBottom", c_int), ("fscore", c_float), ("className", c_char * 50)]


class Struct_TD_VarOut(Structure):
    _fields_ = [("dwObjectSize", c_int), ("pdjToyInfors", Struct_TD_ObjInfor * 128)]


class NLToyDetect:
    """
    物品目标检测
    """
    def __init__(self, libNamePath):
        """
        初始化
        :param libNamePath: 算法so库名称
        """
        if not os.path.exists(libNamePath):
            print("Library file not exit!", libNamePath)
            return -3001
        else:
            self.TD_DLL = cdll.LoadLibrary(libNamePath)

        # 指定函数参数类型
        self.TD_DLL.NL_TD_Command.argtypes = (POINTER(Struct_Handle), c_char_p, c_int, c_float, c_char_p, c_char_p)
        self.TD_DLL.NL_TD_Command.restype = c_int
        self.TD_DLL.NL_TD_Init.argtypes = (POINTER(Struct_Handle),)
        self.TD_DLL.NL_TD_Init.restype = c_int
        self.TD_DLL.NL_TD_Process.argtypes = (
            POINTER(Struct_Handle), POINTER(Struct_TD_VarIn), POINTER(Struct_TD_VarOut))
        self.TD_DLL.NL_TD_Process.restype = c_int
        self.TD_DLL.NL_TD_UnloadModel.argtypes = (POINTER(Struct_Handle),)
        self.TD_DLL.NL_TD_UnloadModel.restype = c_int

        # 初始化结构体变量
        self.djTDHandle = Struct_Handle()  # 结构体变量定义
        self.djTDVarIn = Struct_TD_VarIn()  # 结构体变量定义
        self.djTDVarOut = Struct_TD_VarOut()  # 结构体变量定义

    def NL_TD_ComInit(self, configPath, dwClassNum, dqThreshold, pbyModel, pbyLabel):
        """
        物品目标检测初始化配置，以及加载模型
        :param configPath: 配置文件路径
        :param dwClassNum: 类别数
        :param dqThreshold: 置信度阈值
        :param pbyModel:  模型路径
        :param pbyLabel:  模型label路径
        :return: 返回0，非0负数表示异常
        """
        if not os.path.exists(configPath):
            print("Model file not exit!", configPath)
            return -3501
        else:
            ret = self.TD_DLL.NL_TD_Command(self.djTDHandle, configPath, dwClassNum, dqThreshold, pbyModel, pbyLabel)
            if ret != 0:
                print("NL_TD_Command error code:", ret)
                return ret
        ret = self.TD_DLL.NL_TD_Init(self.djTDHandle)
        if ret != 0:
            print("NL_TD_Init error code:", ret)
            return ret
        return ret

    def NL_TD_InputImg(self, inputImg):
        """
        读取图片
        :param inputImg: 图片路径或图片源
        :return:
        """
        if not os.path.exists(inputImg):
            print("Image file not exit: ")
            return None
        else:
            img = cv2.imread(inputImg)
            if img is None:
                print('image is None')
                return None
            img_len = len(img.shape)
            if img_len == 3:
                srcBGR = img
            else:
                srcBGR = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            return srcBGR

    def NL_TD_InitVarIn(self, srcBGR):
        """
        物品目标检测输入源参数设置
        :param srcBGR: 一帧图片，或者一张图片
        :return: 返回0，非0负数表示异常
        """
        h, w, c = srcBGR.shape
        self.djTDVarIn.dwChannel = c
        self.djTDVarIn.dwWidth = w
        self.djTDVarIn.dwHeight = h
        self.djTDVarIn.pubyIm = srcBGR.astype(np.uint8).tostring()
        if h > 1:
            return 0
        else:
            print("NL_TD_InitVarIn Error!")
            return -1001

    def NL_TD_Process_C(self):
        """
        物品目标检测，主处理函数
        :return: 返回目标个数，非0负数表示异常
        """
        ret = self.TD_DLL.NL_TD_Process(self.djTDHandle, self.djTDVarIn, self.djTDVarOut)
        if ret != 0:
            print("NL_TD_Process error code:", ret)
            return ret
        else:

            return int(self.djTDVarOut.dwObjectSize)

    def NL_TD_Exit(self):
        """
        释放内存与模型
        :return:
        """
        ret = self.TD_DLL.NL_TD_UnloadModel(self.djTDHandle)
        if ret != 0:
            print("NL_TD_UnloadModel error code:", ret)
        return ret
