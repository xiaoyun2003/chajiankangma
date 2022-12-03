from paddleocr import PaddleOCR, draw_ocr
import datetime
import os
import logging
import shutil
#返回识别到的所有文字，按行返回
def PDOCR(ocr,file,isList):
    res=[]
    s=""
    result = ocr.ocr(file, cls=True)
    for line in result[0]:
        s+=line[1][0]
        res.append(line[1][0])
    if isList:
        return res
    else:
        return s


#判断是否已在今天采样，且为阴性,不一定准确,是否锁定今天数据
def isCY(info,isday):
    info=info.replace(" ","").replace("核酸检测","").replace("巳","已").replace("已接种","")
    now=str(datetime.datetime.now().date())
    now=now.replace("2022-","").replace("2023-","")
    if info.find(str(now))==-1 and isday:
        return -2
    if info.find("核酸已采样")!=-1:
        return 200
    if info.find("核酸")!=-1:
        if info.find("已")!=-1:
            if info.find("样")!=-1:
                return 200
    return -1

def pre():
    if not os.path.exists(DATA_path):os.makedirs(DATA_path)
    if not os.path.exists(OK_path):os.makedirs(OK_path)
    if not os.path.exists(UNOK_path):os.makedirs(UNOK_path)

def moveFile(file,path):
    try:
        shutil.move(file,path)
    except Exception as e:
        print(e)



logging.disable(logging.DEBUG) 
logging.disable(logging.WARNING)

#初始化一遍就行
ocr = PaddleOCR(use_angle_cls= False, use_gpu=False,lang="ch") 
#识别一张图片就会转走一张图片到已识别目录。以便程序终止时下次不需要重新识别
#数据目录，截图存放的位置
DATA_path="./D1/"
#已识别的目录
ALAO_path="./已识别图片/"

#合格的图片目录，在已识别目录下面，
OK_path=ALAO_path+"合格截图/"
#不合格的图片目录，在已识别目录下面，
UNOK_path=ALAO_path+"不合格截图/"


#前置检测
pre()


i=1
for file in os.listdir(DATA_path):
    info =PDOCR(ocr,DATA_path+file,False)
    s=isCY(info,False)
    if s==200:
        print(i,"合格",info)
        moveFile(DATA_path+file,OK_path)
    elif s==-1:
        print(i,"未采样或识别出错",info)
        moveFile(DATA_path+file,UNOK_path)
    elif s==-2:
        print(i,"采样时间不在今天",info)
        moveFile(DATA_path+file,UNOK_path)
    elif s==-3:
        print(i,"感染者！！！！",info)
        moveFile(DATA_path+file,UNOK_path)
    i=i+1
