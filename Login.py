# -*- coding: utf-8 -*-

import os, sys, time
import requests
import re
import platform


class HIT_login:
    cfg_dir = str()
    cfg_path = str()
    __users_res = dict()
    current_user = str()
    user_msg = dict()

    def __init__(self, option):
        self.cfg_dir = str(os.path.join(os.path.expanduser("~"), "Hi-Loggin"))
        if "Linux" in platform.platform():
            self.cfg_path = self.cfg_dir + "/login.cfg"
        elif "Windows" in platform.platform():
            self.cfg_path = self.cfg_dir + "\\login.cfg"
        else:
            raise("Unsupport Platform !")
        self.load_cfg()
        if(option == 'auto'):
            self.auto_login()
        elif (option == 'manual'):
            self.manual_login()
        elif (option == 'logout'):
            self.logout()
        else:
            pass

    def load_cfg(self):
        if not os.path.isdir(self.cfg_dir):
            os.mkdir(self.cfg_dir)
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
            self.__users_res[line.split(':')[0]] = line.split(':')[1]
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
            self.current_user = user_id
            return user_id
        else:
            print("Login Error !")

    def auto_login(self):
        print("Auto Mode")
        self.load_cfg()
        for (user_id, pwd) in self.__users_res.items():
            r = self.login_base(user_id, pwd)
            if r['result'] == 'success':
                print("Welcome %s Login Success !" % user_id)
                self.current_user = user_id
                return user_id
        print("Auto LOGIN Fail !")
        
    def logout(self):
        url = 'http://202.118.253.94:8080/eportal/InterFace.do?method=logout'
        res = requests.get(url)
        self.current_user = '-1'
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
    
    def update_info(self):
        self.user_info()


if __name__ == '__main__':
    option = sys.argv[-1]
    s = HIT_login(option)

