# coding=utf-8
import socket
import os
def sendMsg(HOST,data):
    '''
    TCP客户端
    :param data: 字符串数据
    '''
    PORT = 52000
    # 1. 实例化对象
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 2. 连接服务端
    conn.connect((HOST, PORT))  # 连接
    if not data:
        return
    # 3. 发送/接收数据 (发送数据, 接收反馈, 发送反馈, 接收全部数据)
    conn.send(data.encode("utf-8"))  # 发送数据
    data  = conn.recv(1024).decode("utf-8")
    conn.close()  # 关闭连接
    return data

