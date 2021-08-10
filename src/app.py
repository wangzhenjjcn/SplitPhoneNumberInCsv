#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import re
import tkinter.filedialog as tkFileDialog
 



def getPhoneNumber(str):
    if str==None:
        return
    rephone="(?:^|[^\d])(1\d{10})(?:$|[^\d])"
    phone_list=re.compile(rephone).findall(str)
    return phone_list

def getTelNMumber(str):
    if str==None:
        return
    retel="(0\\d{2}-\\d{8}(-\\d{1,4})?)|(0\\d{3}-\\d{7,8}(-\\d{1,4})?)"
 
    tel_list=re.compile(retel).findall(str)
    return tel_list
 

def getNumber(str):
    if str==None:
        return
    rephone="(?<!\d)(1\d{10})(?!\d)"
    phone_list=re.compile(rephone).findall(str)
    return phone_list

def getEMailAddress(str):
    if str==None:
        return
    reemail=re.compile("([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})",re.IGNORECASE)
    mailist=reemail.findall(str.lower())
    return mailist

def choiceFile():
    file_path =  tkFileDialog.askopenfilename(title=u'请选择解析文件', filetypes=(
        ("Csv Files", "*.csv"), ("all files", "*.*")))
    return(file_path)
 

def readFile():
    print("read:%s"%data["filename"])
    firstline=""
    dataline=[]
    with open(data["filename"], 'r+', encoding='GBK') as file_to_read:
        while True:
            lines = file_to_read.readline() 
            if not lines:               
                break
            if firstline=="":
                firstline=lines
                print(firstline)
            else:
                dataline.append(lines)
    data["firstline"]=firstline
    data["filedata"]=dataline
    print("read[%s]lines data"%len(dataline))



def tranceFileData():
    datatrance=[]
    datatrance.append(data["firstline"])
    if data==None:
        return
    if data["filedata"]==None:
        return
    for line in data["filedata"]:
        dataline=str(line)
        nums=getPhoneNumber(line)
        mails=getEMailAddress(line)
        tels=getTelNMumber(line)
        # print("=============================================")
        if len(nums)>0 or len(mails)>0 or  len(tels)>0:
            


            if str(dataline).endswith("\r") or str(dataline).endswith("\n"):
                dataline=str(line).replace("\r\n","").replace("\r","").replace("\n","")
            if not str(dataline).endswith(","):
                dataline=str(line)+",,"

            
            if len(nums)>0:
                for num in nums:
                    if len(num)>3:
                        dataline=dataline+str(num)+","
                        # print(str(num))
            if len(tels)>0:
                for tel in tels:
                    if len(tel)>0:
                        telp=str(tel).split("'")
                        for p in telp:
                            if len(str(p))>3:
                                # print(p)
                                dataline=dataline+str(p)+","
                        # print(str(tel))
            if len(mails)>0:
                for mail in mails:
                    if len(mail)>5:
                        dataline=dataline+str(mail)+","
                        # print(str(mail))
        # print(dataline)
        # print("transout [%s]nums [%s]tels [%s]mails"%(len(nums),len(tels),len(mails)))
        if len(nums)+len(tels)+len(mails)>data["maxd"]:
            data["maxd"]=len(nums)+len(tels)+len(mails)
        datatrance.append(dataline)
    data["datatrance"]=datatrance

def saveFile():
    try:
        d=""
        for i in range(0,data["maxd"]):
            data["firstline"]=data["firstline"]+","
        d=d+str(data["firstline"]).replace("\r\n","").replace("\r","").replace("\n","")+"\r"
        for dt in data["datatrance"]:
            d=d+str(dt).replace("\r\n","").replace("\r","").replace("\n","")+"\r"
        data["savefilename"]=data["filename"]+"-transdata.csv"
        with open(data["savefilename"], 'w+', encoding='GBK') as f:
            f.write(d)
            f.close()
    except Exception as e2:
        print(e2)
        pass 

if __name__ == "__main__":
    
    data={}
    data["title"]={}
    data["filename"]=""
    data["savefilename"]=""
    data["resault"]=""
    data["firstline"]=""
    data["maxd"]=0
 
    try:
        file_path=choiceFile()
        data["filename"]=file_path
        if file_path==None:
            print("file not  exists![%s]"%file_path)
            sys.exit()
        elif not os.path.exists(file_path):
            print("file not  exists![%s]"%file_path)
            sys.exit()
        else: 
            readFile()
            tranceFileData()
            saveFile()
        pass
    except Exception as e:
        print(e)
        sys.exit()
         
