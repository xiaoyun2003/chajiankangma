import requests
import random
import threading
import cv2
import base64
import numpy as np
import urllib
import json
from Crypto.Cipher import AES
import xlrd
from xlutils.copy import copy
import xlwt
import time
import os
import base64
from Crypto.Cipher import AES
import hashlib


h = {
"Authorization": "Basic  YXBwOmFwcA==",
"school": "hbue",
"Content-Length": "0",
"Content-Type": "application/x-www-form-urlencoded",
"Host": "a.sxstczx.com",
"Connection": "Keep-Alive",
"Accept-Encoding": "gzip",
"User-Agent": "okhttp/4.9.0"
}
#login
def login(user,pwd):
    cookie={}
    cookie["host"]="hbue"
    #加密
    pad = lambda s: s + (16 - len(s)%16) * chr(0)
    pwd = pad(pwd)
    aes = AES.new("thanks,pig4cloud".encode(),AES.MODE_CBC,"thanks,pig4cloud".encode())
    en_text = aes.encrypt(pwd.encode())
    pwd = urllib.parse.quote(base64.b64encode(en_text).strip())
    res=requests.get("http://a.sxstczx.com/auth/oauth/token?username="+user+"&password="+pwd+"&grant_type=password",headers=h,cookies=cookie)
    rc=json.loads(res.text)
    if rc!=None and res.status_code!=200:
        print(rc["msg"])
        return False
    else:
        if rc==None:
            rc=res.cookies.get_dict()
        h["authorization"]="Bearer "+rc["access_token"]
        cl={}
        cl["host"]="hbue"
        cl["category"]=str(rc["dept_id"])
        cl["Authorization"]=rc["access_token"]
        return cl



#计算appid
def getAppId(appid,token,timestamp):
    data=appid+token+timestamp
    token_md5=hashlib.md5(token.encode()).hexdigest()
    pwd=token_md5[0:16]
    iv=token_md5[16:32]
    res=hashlib.md5(AES_encrypt(data,pwd,iv).encode()).hexdigest()
    return res

#计算apptoken
def getAppToekn(token,timestamp):
    data=token+timestamp
    token_md5=hashlib.md5(token.encode()).hexdigest()
    pwd=token_md5[0:16]
    iv=token_md5[16:32]
    res=hashlib.md5(AES_encrypt(data,pwd,iv).encode()).hexdigest()
    return res

#获取identify
def getIdentify(cookie,appid,timestamp):
    #计算数据签名
    token=cookie["Authorization"]
    sign=getSign({"runType":"1"},getAppId(appid,token,timestamp),getAppToekn(token,timestamp),timestamp,token)
    h["sign"]=sign
    h["timestamp"]=timestamp
    res=requests.get("http://a.sxstczx.com/exercise/exerciseSetting/getSetting?runType=1",headers=h,cookies=cookie)
    if res.status_code==200:
        jres=json.loads(res.text)
        return jres
    else:
        print(res.text)
        return False




#上传数据
def upload(cookie,data_dict):
    #计算数据签名
    sign=getSign(data_dict,getAppId(appid,token,timestamp),getAppToekn(token,timestamp),timestamp,token)
    #进行url编码
    data_dict=URL_encode(data_dict)
    #设置请求头
    h["sign"]=sign
    h["timestamp"]=timestamp
    data=dict2str(data_dict)
    res=requests.post("http://a.sxstczx.com/exercise/exerciseRecord/addExerciseRecord",data=data,headers=h,cookies=cookie)
    if res.status_code==200:
        return json.loads(res.text)
    else:
        print(res)
        return False


#计算sign
def getSign(data_d,appId,appSecret,timestamp,token):
    data_d["appId"]=appId
    data_d["appSecret"]=appSecret
    sres=sorted(data_d.items(), reverse=False)
    s=""
    for i in sres:
        s+="&"+i[0]+"="+i[1]
    data=s[1:]
    pwd=hashlib.md5(token.encode()).hexdigest()[0:16]
    iv=hashlib.md5(token.encode()).hexdigest()[16:32]
    res=hashlib.md5(AES_encrypt(data,pwd,iv).encode()).hexdigest()
    return res

def URL_encode(data_dict):
    for k,v in data_dict.items():
        data_dict[k]=urllib.parse.quote(v,encoding="utf-8")
    return data_dict

#字典转文本
def dict2str(data_dict):
    s=""
    for k,v in data_dict.items():
        s+="&"+k+"="+v
    return s[1:]



#文本转字典
def str2dict(data):
    if data.find("&")==-1:
        if data.find("=")!=-1:
            return {data.split("=")[0]:data.split("=")[1]}
        else:
            return data
    dl=data.split("&")
    dict1={}
    for i in dl:
        if i!=None and i.find("=")!=-1:
            ss=i.split("=")
            dict1[ss[0]]=ss[1]
    return dict1

#读取文件
def file_read(file):
    with open(file,'r') as f:
        res= f.read()
        res=res.replace("\\","")
        return res
    
def AES_encrypt(data,pwd,iv):
    BLOCK_SIZE = 16  # Bytes
    # 数据进行 PKCS5Padding 的填充
    pad = lambda s: (s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE))
    raw = pad(str(data))
    # 通过key值，使用ECB模式进行加密
    cipher = AES.new(pwd.encode(), AES.MODE_CBC,iv.encode("utf-8"))
    # 得到加密后的字节码
    encrypted_text = cipher.encrypt(bytes(raw, encoding='utf-8'))
    # 字节码转换成十六进制  再转成 字符串
    AES_en_str = base64.b64encode(encrypted_text)
    # 最后将密文转化成字符串
    AES_en_str = AES_en_str.decode("utf-8")
    return AES_en_str

    




#完成登录，返回加密凭证token
cl=login("22080006","XY200303.")
if not cl:
    print("密码错误")
    print(cl)
    exit()




token=cl["Authorization"]

#时间戳
timestamp=str(int(round(time.time() * 1000)))

#appid
appid="c9292ee89d2f49492f983f5931af0d09"

#获取标识
indentify=getIdentify(cl,appid,timestamp)
print(indentify)
#上传的数据的文本形式
data='appVersion=1.7.7&avgSpeed=0.0&brand=Vivo&endTime=1669380398045&geofence=&gitudeLatitude=&identify=8dcaa7e7-2d51-4ef3-9634-1d7c285e1c50&isFaceStatus=1&isSequencePoint=0&model=Vivo X9Plus L&okPointList=[]&pointList=[]&speed=0\'0"&sportRange=0.000&sportTime=375&sportType=1&startTime=1669380393377&stepNumbers=[0]&system=Android&uploadType=0&version=7.1.2'


#文本转字典，方便操作
data_dict=str2dict(data)

#跑步的标识
data_dict["identify"]=indentify["data"]["identify"]




#构建需要修改的数据集，按需更改
#跑步的平均速度
time=int(round(time.time() * 1000))
data_dict["avgSpeed"]="10.0300000000"





#跑步的开始时间
data_dict["startTime"]=str(time)

#跑步间隔时间,默认秒为单位
#9分43秒
sport_time=9*60+21

#模拟跑步间隔，服务端会记录提交时间，如果跑步结束时间在提交时间之后会出问题

#print("正在运动中...，请耐心等待",sport_time,"s")
#time.sleep(int(sport_time/2))
print("运动结束...")

#跑步的运动时长
data_dict["sportTime"]=str(int(sport_time))


#跑步的结束时间
data_dict["endTime"]=str(time+sport_time*1000)



#跑步的轨迹数据
git=json.loads(file_read("./sport.txt"))


data_dict["geofence"]=json.dumps(indentify["data"]["geofence"])


data_dict["gitudeLatitude"]=json.dumps(git)


#跑步的距离
data_dict["sportRange"]="1.533"


#跑步的速度
data_dict["speed"]="05'19\""
#设备的品牌
data_dict["brand"]="Vivo"

#设备型号
data_dict["model"]="Vivo X9Plus L"
#跑步的步数
step=1412
data_dict["stepNumbers"]="["+str(step)+"]"




#上传
r=upload(cl,data_dict)

if r:
    print("记录上传成功")
    print(r)
else:
    print("记录上传失败")
    print(r)