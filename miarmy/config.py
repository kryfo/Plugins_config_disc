#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import sys
import os
import shutil
import subprocess
from imp import reload
reload(sys)
# sys.setdefaultencoding('utf-8')
from MayaPlugin import PluginBase


class MiarmyConfig():
    def __init__(self,clientInfo):
        # self.MyLog(clientInfo)
        self.cgName = clientInfo['cgName']
        self.cgVersion = clientInfo['cgVersion']
        self.pluginName = clientInfo['pluginName']
        self.pluginVersion = clientInfo['pluginVersion']
        self.plugins = clientInfo['plugins'] #dict
        self.userId = clientInfo['userId']
        self.taskId = clientInfo['taskId']  

        #import 公共使用的函数 PluginBase  ，配置脚本（W2        B:/plugins/maya_new/envInfo.json）信息获取，清理目录，创建目录，找相同命名的压缩包，拷贝文件，拷贝目录，解压文件，编码转换，MD5值校验   
        self.Base = PluginBase()
        
        #获取本地D盘插件路径
        self._PluginDir = os.path.join(self.Base.get_json_ini('Node_D'),'miarmy','software',self.cgName + self.cgVersion + '_' + self.pluginName + self.pluginVersion).replace('\\','/')
        self.MyLog(self._PluginDir)

    def MyLog(self,message,extr="miarmySetup"):      
        if str(message).strip() != "":
            print("[%s] %s"%(extr,str(message)))

    def reCreateMod(self):
        DOME_ROOT_DIR = self._PluginDir
        DOME_ROOT_DIR = DOME_ROOT_DIR.replace("/","\\")
        #mod文件
        MAYA_MODULES_FILE = self._PluginDir + r"/maya%s/maya_root/modules/MiarmyForMaya.txt"%(self.cgVersion)
        PUBLIC_MODULES_FILE = self._PluginDir + r"/maya%s/maya_root/modules/MiarmyPublic.txt"%(self.cgVersion)
            
        MODULES_LOCAL = self._PluginDir + r"/%s/maya_root/modules"%(self.cgVersion)
        MODULES_LIST =[MAYA_MODULES_FILE,PUBLIC_MODULES_FILE]
        MODULES_KEY = ""
        for elm in MODULES_LIST:
            MODULE_NAME = os.path.basename(elm)
            if MODULE_NAME == "MiarmyForMaya.txt":
                MODULES_KEY = "Miarmy"
            elif MODULE_NAME == "MiarmyPublic.txt":
                MODULES_KEY = "MiarmyPublic"

            if os.path.exists(elm):
                fp = open(elm,'r')
                lines = fp.readlines()
                fp.close()
                #路径是否有问题?
                lines[0] = "+ %s Any %s \n"%(MODULES_KEY,MODULES_LOCAL)
                fp = open(elm,'r+')
                for s in lines:
                    fp.writelines(s)
                fp.close() 
            else:
                self.MyLog ("\n module file don't exist: \n" + elm)



    def EnvSetup(self):
# set miarmy aut_load use usersetup.mel
        _MAYA_SCRIPT_PATH=os.environ.get('MAYA_SCRIPT_PATH')
        #usersetup.mel 读这个有用?
        os.environ['MAYA_SCRIPT_PATH'] = (_MAYA_SCRIPT_PATH + r";"  if _MAYA_SCRIPT_PATH else "") + self._PluginDir +"/usesetup/"
#set autlode in plugins.mel

        #设置插件 开maya时 自动开启
        hasPlugPrefs = False
        if self.cgVersion <= '2015':
            self.cgVersion = "%s-x64" % self.cgVersion

        pluginPrefsFile = r"C:\users\enfuzion\Documents\maya\%s\prefs\pluginPrefs.mel" % (self.cgVersion)
        plug_load  = (r'evalDeferred("autoLoadPlugin(\"\", \"MiarmyPro\", \"MiarmyPro\")");'+'\n')
        self.MyLog ("MiarmyProForMaya%s" % (self.cgVersion))
        with open(pluginPrefsFile, "a+") as f:
            lines = f.readlines()
            for line in lines:
                if plug_load == line.strip():
                    self.MyLog ("yes MiarmyProForMaya ")
                    hasPlugPrefs = True
            if not hasPlugPrefs:
                self.MyLog ("write MiarmyProForMaya")
                f.write(plug_load)
#set others plugins's env >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        pluginList = self.plugins
        renderSoftware_ver = self.cgVersion
        if pluginList:

            if 'mtoa' in pluginList:
                #对应arnold版本的 dll
                srcDir= self._PluginDir + r"/maya_miarmy/bin/arnold"  
                #C盘路径
                dstDir=r'"C:/Program Files/Basefount/Miarmy/bin/arnold"' 
                #拷贝过去 
                os.system ("robocopy /S /NDL /NFL  %s %s" % (srcDir, dstDir))
                self.MyLog ("arnold and miarmy env set finish!!!") 

            if 'vrayformaya' in pluginList:
                self.MyLog ("**********************Set miarmy for vray dso env**************************************")
                #确认vray版本
                vray_ver= pluginList['vrayformaya'][:3]

                #找到对应的 vray_geomMcdVRGeom2.dll 将路径添加进环境变量
                #miarmy_root 没定义
                vray_plug_path=miarmy_root+"\\maya_miarmy\\bin\\vray\\vray_"+vray_ver
                if float(vray_ver) == 2.4:
                    vray_plug_path = vray_plug_path
                elif float(vray_ver) == 3.0 : 
                    if int(renderSoftware_ver[:4])<=2014:
                        vray_plug_path+="\Maya2014"
                    else:
                        vray_plug_path+="\Maya2015and2016"
                elif float(vray_ver) >=3.1:
                    vray_plug_path=miarmy_root+"\\maya_miarmy\\bin\\vray\\vray_3.1-3.5"
                    if int(renderSoftware_ver[:4])<=2014:
                        
                        vray_plug_path+="\Maya2014"
                    else:
                        vray_plug_path+="\Maya2015-2017"
                else:
                    pass
                self.MyLog (vray_plug_path)


                VRAY_FOR_Maya_env="VRAY_FOR_Maya%s_PLUGINS_x64" %(renderSoftware_ver) 
                self.MyLog (VRAY_FOR_Maya_env)
                #应该写错了吧
                if not os.environ.has_key('VRAY_FOR_Maya_env'):
                    os.environ[VRAY_FOR_Maya_env] = vray_plug_path
                else:
                    os.environ[VRAY_FOR_Maya_env] = os.environ.get(VRAY_FOR_Maya_env)+r";"+vray_plug_path
                self.MyLog (os.environ.get(VRAY_FOR_Maya_env))
                #添加另一条变量
                _MAYA_SCRIPT_PATH=os.environ.get('MAYA_SCRIPT_PATH')
                os.environ['MAYA_SCRIPT_PATH'] = (_MAYA_SCRIPT_PATH + r";"  if _MAYA_SCRIPT_PATH else "") + miarmy_root+"/usesetup/"


def main(*args):
    # NEWEST_MIARMY = "6.2.18"
    # configPlugin.MyLog("ORL:\n" + args[0])
    infoDict = args[0]
    # infoDict =infoDict.replace((infoDict.['plugins']['miarmy']),NEWEST_MIARMY)    
    configPlugin = MiarmyConfig(infoDict)
    # configPlugin.MyLog("NOW:\n" + infoDict)
    configPlugin.reCreateMod()
    configPlugin.EnvSetup()
    configPlugin.MyLog( "set miarmy env finish")



if __name__ == '__main__':
    main()
    # os.system ("\""+MAYA_ROOT + "/bin/maya.exe"+"\"")