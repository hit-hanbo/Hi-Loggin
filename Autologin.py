# -*- coding: utf-8 -*-

import os, sys, time
import requests
import re
import tkinter
import threading

class HIT_login:
    cfg_path = str()
    users_res = dict()
    current_user = str()
    net_stat = 0
    user_msg = dict()

    def __init__(self, option):
        self.cfg_path = str(os.path.join(os.path.expanduser("~"), 
                            "Documents")) + "\\login.cfg"
        self.load_cfg()
        os.system("a")
        if(option == 'auto'):
            self.auto_login()
        elif (option == 'manual'):
            self.manual_login()
        elif (option == 'check'):
            self.net_stat()
        elif (option == 'logout'):
            self.logout()
        else:
            pass
        if(self.net_stat == 1):
            self.user_info()     

    def load_cfg(self):
        if os.path.isfile(self.cfg_path):
            cfg_file = open(self.cfg_path, mode="r+", encoding='UTF-8')
        else:
            cfg_file = open(self.cfg_path, mode='x+', encoding='UTF-8')
            cfg_file.write("#配置文件格式为\"用户名:密码\",每行可以保存一个用户,如\n")
            cfg_file.write("#123:456\n#789:qwe")

        for line in cfg_file.readlines():
            line = line.strip()
            if (not len(line)):
                continue
            elif '#' in line:
                continue
            self.users_res[line.split(':')[0]] = line.split(':')[1]
        cfg_file.close()

    def login_base(self, username, password):
        url = 'http://123.123.123.123'
        pattern = re.compile(r"wlanuserip.*'")
        portal_url = 'http://202.118.253.94:8080/eportal/InterFace.do?method=login'
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        string = pattern.findall(r.text)[0][0:-1]
        data = {
            "userId": username,
            "password": password,
            "service": "",
            "queryString": string,
            "operatorPwd": "",
            "operatorUserId": "",
            "validcode": "",
        }
        result = requests.post(portal_url, data=data)
        #print("usr"+username+"pwd"+password)
        return result.json()

    def manual_login(self):
        user_id = input("Input Your Username :")
        pwd = input("Input Password :")
        r = self.login_base(username=user_id, password=pwd)
        if r['result'] == 'success':
            print("Welcome %s Login Success !" % user_id)
        else:
            print("Login Error !")

    def auto_login(self):
        print("Auto Mode")
        self.load_cfg()
        for (user_id, pwd) in self.users_res.items():
            r = self.login_base(user_id, pwd)
            if r['result'] == 'success':
                print("Welcome %s Login Success !" % user_id)
                self.current_user = user_id
        print("Auto LOGIN Fail !")
        self.test_internet()
        
    def logout(self):
        url = 'http://202.118.253.94:8080/eportal/InterFace.do?method=logout'
        res = requests.get(url)
        return 1

    def user_info(self):
        url = "http://202.118.253.94:8080/eportal/InterFace.do?method=getOnlineUserInfo"
        pattern = re.compile(r"(?<==).*")
        res = requests.get("http://202.118.253.94:8080")
        user_index = pattern.findall(res.url)[0]
        post_data = "userIndex=" + str(user_index)
        res = requests.post(url, data=post_data)
        res.encoding = res.apparent_encoding
        self.user_msg = res.json()
        return self.user_msg

    def killall(self, username, password):
        url = "http://202.118.253.94:8080/eportal/InterFace.do?method=logoutByUserIdAndPass"
        post_data = "userId=" + str(username) + "&pass=" + str(password)
        res = requests.post(url, data=post_data)

    def test_internet(self):
        url = "http://www.baidu.com"
        text = requests.get(url).text[0:200]
        pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
        IP = pattern.findall(text)
        if(IP == "202.118.253.94"):
            self.net_stat = 0
            return 0
        else:
            self.net_stat = 1
            return 1
        
class GUI:
    user_msg = dict()
    internet = int()

    def __init__(self):
        root = tkinter.Tk()
        root.title("HIT-WLAN 登陆工具")
        root.geometry('720x560')
        #初始化布局添加处
        #添加两行，显示登陆的账号，到期时间和IP
        self.show_info = tkinter.StringVar()
        self.show_info.set("\n Loading ···")
        current_user = tkinter.Label(root, textvariable=self.show_info, 
                                    font=('Arial', 16))
        current_user.pack()
        #显示一张图片
        img_file = tkinter.PhotoImage(file=sys.path[0]+"\\HIT.gif")
        img_label = tkinter.Label(root, image=img_file)
        img_label.pack()
        #添加5个按钮：自动连接、手动连接、注销、编辑用户信息、关于
        Button1_Auto = tkinter.Button(root, text="自动登陆", command=self.Button_auto, width=50)
        Button1_Auto.pack()
        Button2_Manual = tkinter.Button(root, text="手动登陆", command=self.Button_manual, width=50)
        Button2_Manual.pack()
        Button3_Logout = tkinter.Button(root, text="注销", command=self.Button_logout, width=50)
        Button3_Logout.pack()
        Button4_Edit = tkinter.Button(root, text="编辑用户信息", command=self.Button_Edit, width=50)
        Button4_Edit.pack()
        Button5_About = tkinter.Button(root, text="关于", command=self.Button_About, width=50)
        Button5_About.pack()
        self.Obj_usr = HIT_login("other")
        refresh = threading.Thread(target=self.user_show)
        refresh.start()
        self.internet = self.Obj_usr.test_internet()
        root.mainloop() 

    def user_show(self):
        while(True):
            try:
                self.Obj_usr.user_info()
                self.user_msg = self.Obj_usr.user_msg
                if(self.internet == 1):
                    self.show_info.set("\n欢迎 " + str(self.user_msg["userName"]) + "\n" +
                                        "距离到期还有" + str(self.user_msg["maxLeavingTime"]))
                else:
                    self.show_info.set("未连接到HIT-WLAN，请连接。")
                print("正常获取info")
            except:
                self.show_info.set("未登录HIT-WLAN，选择下方选项登陆。")
                print("连接但未登录")
            time.sleep(1)

    def Button_auto(self):
        thread_login = threading.Thread(target=self.Obj_usr.auto_login)
        thread_login.start()
    
    def Button_manual(self):
        manual = tkinter.Tk()
        manual.title("HIT-WLAN手动工具")
        manual.geometry("240x150")
        user_notice = tkinter.Label(manual, text="用户名:")
        user_notice.grid(row=0, sticky=tkinter.W)
        username = tkinter.Entry(manual)
        username.grid(row=0, column=1, sticky=tkinter.E)

        pwd_notice = tkinter.Label(manual, text="密码:")
        pwd_notice.grid(row=1, sticky=tkinter.W)
        password = tkinter.Entry(manual, show='*')
        password.grid(row=1, column=1, sticky=tkinter.E)

        button_login = tkinter.Button(manual, text="登陆", width=20, 
                                        command=lambda: (self.Obj_usr.login_base(username=username.get(), password=password.get())) or manual.destroy())
        button_login.grid(column=1)
        button_killall = tkinter.Button(manual, text="下线所有设备", width=20, 
                                        command=lambda: (self.Obj_usr.killall(username=username.get(), password=password.get())) or manual.destroy())
        button_killall.grid(column=1)
        manual.mainloop()

    def Button_logout(self):
        thread_logout = threading.Thread(target=self.Obj_usr.logout)
        thread_logout.start()

    def Button_About(self):
        os.system("start http://www.sdawn.me/index.php/2018/06/17/python-hit-gui/")

    def Button_Edit(self):
        thread_editor = threading.Thread(target=lambda:os.system("notepad " + self.Obj_usr.cfg_path))
        thread_editor.start()

if __name__ == '__main__':
    window = GUI()
    user = HIT_login("other")
    
