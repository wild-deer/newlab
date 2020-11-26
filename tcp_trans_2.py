

import socket
import json
import time
import random
from threading import Thread



host = "117.78.1.201" #AIOT云平台tcp连接host地址
port = 8700           #AIOT云平台tcp连接port



def socket_client(host,port):
    ''''
    创建TCP连接
    '''
    handshare_data = {
            "t": 1,                                    #固定数据代表连接请求
            "device": "jeremy233",                 #设备标识
            "key": "f38582aea15c47bd89c4844f4eecbc0d", #传输密钥
            "ver": "v1.0"}                             #客户端代码版本号,可以是自己拟定的一组客户端代码版本号值
    try:
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #创建socket
        tcp_client.connect((host,port))                                #建立tcp连接
        tcp_client.send(json.dumps(handshare_data).encode())           #发送云平台连接请求
        res_msg = tcp_client.recv(1024).decode()                       #接收云平台响应
    except Exception as e:
        print(e)
        return False
    return tcp_client                                                  #返回socket对象


def listen_server(socket_obj):
    '''
    监听TCP连接服务端消息
    :param socket_obj:
    :return:
    '''
    while True:
        try:
            res = socket_obj.recv(1024).decode() #接收服务端数据
            if not res:
                exit()
        except Exception as e:
            print(e)
            exit()


def tcp_ping(socket_obj):
    '''
    TCP连接心跳包
    :param socket_obj:
    :param obj:
    :return:
    '''
    while True:
        try:
            socket_obj.send("$#AT#".encode())   #发送心跳包数据
            time.sleep(30)
        except Exception as e:
            print(e)
            exit()



def send_carNumber(tcp_client,road,num):
    '''

    :param tcp_client: socket对象
    :param num: 车辆数
    :return:
    '''

    data = {
        "t": 3,
        "datatype": 1,
        "datas": {
            road:num,
        },
        # "msgid": str(random.randint(100,100000))
    }
    try:
        tcp_client.send(json.dumps(data).encode())       #发送数据
    except Exception as e:
        print(e)




def init_tcp():
    tcp_client = socket_client(host, port)  # 创建tcp　sockt 对象
    t1 = Thread(target=listen_server, args=(tcp_client,))  # 监听服务端发送数据
    t1.start()
    t2 = Thread(target=tcp_ping, args=(tcp_client,))  # 创建与云平台保持心跳的线程
    t2.start()
    return tcp_client




if __name__ == '__main__':
    i=0
    tcp_client = init_tcp()
    while(1):
        i = i+1
        time.sleep(10)
        print(i)
        send_carNumber(tcp_client,"car2" ,i)  # 发送一条体温数据