import socket
from threading import  Thread
import re
import time
from PyQt5.QtSql import *
import pymysql

socket_user=dict()  #socket到用户的映射
online_socket=list() #存储在线用户

def check_user(username,psw):
    """
    检测用户登录时输入的用户名和密码是否正确
    :param username: 待检查的用户名
    :param psw: 待检查的用户密码
    :param status:判断是否在线
    :return: 用户名和密码是否通过的结果
    """
    db=None
    results=None
    try:
        db=pymysql.connect(host='localhost',user='root',password='139739',port=3306,db='test3')
        cursor=db.cursor()
        sql="select * FROM mysock where useid='%s'" % (username)
        cursor.execute(sql)
        results=cursor.fetchone()
        print(results)

    except Exception as e:
        print(e)
    db.close()
    print("end")
    if(results==None):         #不能把None 赋给多个值，所以就首先判断这一句
        print("s3")
        return "账号不存在"
    elif(username==results[0] and psw==results[1]):
        print("s1")
        return "登录成功"
    elif(username==results[0] and psw!=results[1]):
        print("s2")
        return "密码错误"


def handle_login(new_socket):
    """
    处理登录请求
    :param new_socket: 用户连接时生成的套接字
    """
    username_psw=new_socket.recv(1024).decode("utf-8")
    username_psw=username_psw.split(' ')
    husername=str(username_psw[0])
    hpassword=str(username_psw[1])
    check_result=check_user(husername,hpassword)
    new_socket.sendall(check_result.encode("utf-8"))
    if check_result=="登录成功":
        socket_user[new_socket]=husername
        online_socket.append(new_socket)
        update_online_list()
        time.sleep(3)
        online_notice(new_socket)


def update_online_list():
    """
    发送所有在线用户列表类型
    总和不会超过1024byte
    更新客户端在线用户列表
    """
    online_usernames=""
    for s in online_socket:
        online_usernames+=socket_user[s]+"#!"
    for socket in online_socket:
        socket.sendall(("#!onlines#!"+online_usernames).encode("utf-8"))

def online_notice(new_socket):
    """
    给所有在线客户端发送新客户端上线的通知
    :param new_socket: 新用户上线的套接字
    """
    welcome_str="*******Welcome "+socket_user[new_socket]+" come to MyChat!********"

    for socket in online_socket:
        socket.sendall(("#!notices#!"+welcome_str).encode("utf-8"))

def offline_notice(offline_socket):
    """
    给所有在线用户发送用户离线通知
    :param offline_socket: 离线用户对应的套接字
    """
    left_str="******"+socket_user[offline_socket]+"has left *******"
    for socket in online_socket:
        socket.sendall(("#!notices#!"+left_str).encode("utf-8"))




def handle_msg(new_socket):
    """
    发送的消息类型的内容总和不超过1024byte
    对客户端要发送的内容进行广播
    :param new_socket: 要发送信息的客户端的套接字
    如果要单独发送，可以写一个源客户端和目的客户端
    """
    content=new_socket.recv(1024).decode("utf-8")
    for socket in online_socket:
        socket.sendall(("#!message#!"+socket_user[new_socket]+"#!"+content).encode("utf-8"))



def handle(new_socket,addr):
    """
    服务器运行的主框架
    :param new_socket: 本次连接的客户端套接字
    :param addr: 本次连接客户端的ip和port
    """

    try:
        while True:
            req_type=new_socket.recv(1).decode("utf-8")  #获取请求类型
            if req_type:              #如果不为真，则说明客户端已断开
                if req_type=="1":     #登录请求
                    print("开始处理登录请求")
                    handle_login(new_socket)
                elif req_type=="3":
                    print("开始处理发送信息请求")
                    handle_msg(new_socket)
            else:
                break

    except Exception as ret:
        print(str(addr)+" 连接异常，准备断开"+str(ret))
    finally:
        try:
            #客户端断开后执行的操作
            new_socket.close()
            online_socket.remove(new_socket)
            offline_notice(new_socket)
            socket_user.pop(new_socket)
            time.sleep(6)
            update_online_list()
        except Exception as ret:
            print(str(addr)+"连接关闭")


if __name__ == '__main__':
    try:
        main_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        main_socket.bind(('localhost',64208))                      #服务器绑定的ip和port
        main_socket.listen(128)  #最大挂起数
        print("服务器启动成功")
        while True:
            new_socket,addr=main_socket.accept()
            thread=Thread(target=handle,args=(new_socket,addr)).start()
    except Exception as ret:
        print("服务器运行错误：" +str(ret))
