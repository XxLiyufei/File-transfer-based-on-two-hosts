#!/usr/bin/env python
# -*- coding=utf-8 -*-

"""
file: fserver.py
socket service
"""

import socket #socket模块
import threading #threading模块
import time #time模块
import sys #sys模块
import os #os模块
import struct #struct模块

def socket_service():#创建服务端
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket.AF_INET建立服务器间网络通信，socket.SOCK_STREAM为流式socket，for TCP
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #（一般不会立即关闭而经历TIME_WAIT的过程）后想继续重用该socket
        s.bind(('192.168.125.139', 6666)) #将套接字绑定到地址，在AF_NET下，以元组(host，port)的形式表示地址
        s.listen(10) #开始监听TCP传入连接，s.listen(backlog)格式，backlog指定在拒绝连接之前，OS可以挂起的最大连接数
    except socket.error as msg: # 防止socket server重启后端口被占用（socket.error: [Errno 98] Address already in use
        print msg
        sys.exit(1)
    print '等待连接...'

    while 1:
        conn, addr = s.accept() #连接地址
        t = threading.Thread(target=deal_data, args=(conn, addr)) #线程等待处理传送的文件
        t.start()

def deal_data(conn, addr): #文件传输
    print '接受到新连接来自 {0}'.format(addr)
    #conn.settimeout(500)
    conn.send('欢迎进入本服务器')

    while 1:
        fileinfo_size = struct.calcsize('128sl') #限定文件大小
	#128s表示文件名为128bytes长，l表示一个int或log文件类型
        buf = conn.recv(fileinfo_size) #设定缓冲区大小
        if buf:
            filename, filesize = struct.unpack('128sl', buf)
            fn = filename.strip('\00') #文件结束
            new_filename = os.path.join('./', 'new_' + fn) #写入服务端时重命名文件为new_file.xxx
            print 'file new name is {0}, filesize if {1}'.format(new_filename,
                                                                 filesize)

            recvd_size = 0  # 定义已接收文件的大小
            fp = open(new_filename, 'wb') #写入文件到服务端，wb表示以二进制形式写
            print '开始接收文件...'

            while not recvd_size == filesize: #视文件大小不同情况进行不同操作
                if filesize - recvd_size > 1024:
                    data = conn.recv(1024)
                    recvd_size += len(data)
                else:
                    data = conn.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data) 
            fp.close() #传送关闭
            print '文件传送结束...'
        conn.close()
        break


if __name__ == '__main__':
    socket_service()
