# coding=utf-8
# socket_demo.py 套接字接口
# 协议: TCP/IP(3次握手,4次断开) UDP(直接发数据)
# 一台PC最多可开 65535 个端口

import socket
import os
from file_data import *
from sub_process import *
from userinfo import *


# 地址簇
socket.AF_INET  # IPV4, (host, port), host:'' / '127.0.0.1'
socket.AF_INET6  # IPV6, (host, port, flowinfo, scopeid); boolean = socket.has_ipv6 // 是否支持ipv6

# 套接字类型
socket.SOCK_STREAM  # tcp
socket.SOCK_DGRAM  # udp
socket.SOCK_RAW  # 原始套接字(可伪造IP地址,发起DDOS攻击)
socket.SOCK_RDM  # UDP,保证交付,但不保证顺序
socket.SOCK_SEQPACKET


HOST = '0.0.0.0' # windows: '127.0.0.1' / 'localhost'; linux:0.0.0.0
PORT = 52000


def tcp_server():
    '''
    TCP服务端
    '''

    # 1. 实例化socket对象
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 可重用地址
    # 2. 绑定
    server.bind((HOST, PORT))  # 绑定
    # 3. 监听链接
    server.listen()
    while True:
        # 4. 接收一个连接
        conn, addr = server.accept()  # (阻塞等待)接收一个连接, 返回 连接对象 地址
        while True:
            # 5. 接收/发送数据 (接收数据(命令), 发送数据量, 接收反馈, 发送全部数据)
            data_bytes = conn.recv(1024)  # (阻塞)接收数据
            if not data_bytes:
                break  # 当client断开时,conn.recv不断的接收空信息
            data_str = data_bytes.decode("utf-8")

            if data_str == 'getinfo':
                try:
                    path,md5,sha1=getData()
                    filepath,filename  = os.path.split(path)
                    username = getUserName()
                    conn.send((filename+' '+md5+' '+sha1 + ' '+username).encode("utf-8"))
                except:
                    conn.send('error'.encode("utf-8"))
            elif data_str == 'install':
                try:
                    install(path)
                except:
                    conn.send('error'.encode("utf-8"))


        conn.close()
    server.close()

if __name__ == "__main__":
    while True:
        # TCP
        try:
            tcp_server()

        except :
            pass