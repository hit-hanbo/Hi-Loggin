# -*- coding: utf-8 -*-

import tkinter
import os, sys

class GUI:
    user_msg = dict()
    internet = int()

    def __init__(self):
        root = tkinter.Tk()
        root.title("HIT-WLAN 登陆工具")
        root.geometry('720x520')
        #初始化布局添加处
        #添加两行，显示登陆的账号，到期时间和IP
        self.show_info = tkinter.StringVar()
        self.show_info.set("\n Loading ···")
        current_user = tkinter.Label(root, textvariable=self.show_info, 
                                    font=('Arial', 16))
        current_user.pack()
        #显示一张图片
        print()
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

        root.mainloop()

    def user_show(self):
        if(self.internet == 1):
            self.show_info.set("\n欢迎 " + str(self.user_msg["userName"]) + "\n" +
                                "距离到期还有" + str(self.user_msg["maxLeavingTime"]))
        else:
            self.show_info.set("未连接到HIT-WLAN，请连接。")

    def Button_auto(self):
        pass
    
    def Button_manual(self):
        pass

    def Button_logout(self):
        pass

    def Button_About(self):
        pass

    def Button_Edit(self):
        pass

if __name__ == "__main__":
    windows = GUI()
    