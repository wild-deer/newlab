import time

import requests

class req:

    def __init__(self):

        self.accesstokeon = None
        self.head = None


        data = {'Account': '15328649221',  # 用户名
                'Password': 'YJLs13981383032',  # 密码
                'rememberme': 'true'}
        r = requests.post('http://api.nlecloud.com/Users/Login', data=data).json()  # 发送data并将返回值以json格式存入 r 中
        self.accesstokeon = r['ResultObj']['AccessToken']  # 储存AccessToken

        self.head = {'AccessToken': self.accesstokeon}  # 将AccessToken放入请求头中
    def get_info(self,deviceid,sensor):
        # 获得传感器信息的函数
        try:



            # 请求体
            # update = {"DatasDTO": [{"ApiTag": "car",
            #                         "PointDTO": [{
            #                             "Value": value}
            #                         ]
            #                         }
            #                        ]
            #           }

            # resp = requests.post('http://api.nlecloud.com/devices/122944/datas', json=update, headers=self.head)  # 发送请求
            # resp2 = requests.post('http://api.nlecloud.com/Cmds?deviceId=122944&apiTag=led_1',json =update2 , headers=head)  # 发送请求
            resp3 = requests.get("http://api.nlecloud.com/devices/" + deviceid + "/Sensors/" + sensor,headers = self.head).json()# 获得传感器信息
            state = resp3['ResultObj']['Value']
            print(state)
        except Exception as e:
            print(e)
            return False
    def setinfo(self,deviceid,sensor,value):
            # 设置执行器信息
            update2 = value
            resp2 = requests.post('http://api.nlecloud.com/Cmds?deviceId='+ deviceid +'&apiTag=' + sensor,json =value , headers=self.head)  # 发送请求
            try:
                pass

            except Exception as e:
                print(e)
                return False

if __name__ == '__main__':
    requst = req()
    i = 1
    while(1):
        requst.get_info("122944","led_1")
        i = i+1
        time.sleep(3)