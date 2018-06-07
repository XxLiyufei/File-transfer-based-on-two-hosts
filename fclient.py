
#!/usr/bin/env python  
# -*- coding=utf-8 -*-  
  
  
""" 
file: fclient.py 
socket client 
"""  
  
import socket #socket模块  
import os #os模块  
import sys #sys模块  
import struct #struct模块  
  
  
def socket_client(): #创建客户端  
    try:  
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket.AF_INET建立服务器间网络通信，socket.SOCK_STREAM为流式socket，for TCP  
        s.connect(('192.168.125.139', 6666)) #连接到服务器，端口号为6666  
    except socket.error as msg: #防止socket server重启后端口被占用  
        print msg  
        sys.exit(1)  
  
    print s.recv(1024)  
  
    while 1:  
        filepath = raw_input('请输入文件路径： ')  
        if os.path.isfile(filepath):  
            # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小  
            fileinfo_size = struct.calcsize('128sl')  
            # 定义文件头信息，包含文件名和文件大小  
            fhead = struct.pack('128sl', os.path.basename(filepath),  
                                os.stat(filepath).st_size)  
            s.send(fhead)  
            print '客户端文件路径: {0}'.format(filepath)  
  
            fp = open(filepath, 'rb') #读出文件,rb以二进制读模式打开  
            while 1:  
                data = fp.read(1024)  
                if not data:  
                    print '{0} 文件发送结束...'.format(filepath)  
                    break  
                s.send(data)  
        s.close() #传送关闭  
        break  
  
  
if __name__ == '__main__':  
    socket_client()  
