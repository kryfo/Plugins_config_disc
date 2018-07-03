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


class GolaemCrowdConfig():
    def __init__(self,clientInfo):
        # self.MyLog(clientInfo)
        self.cgName = clientInfo['cgName']
        self.cgVersion = clientInfo['cgVersion']
        self.pluginName = clientInfo['pluginName']
        self.pluginVersion = clientInfo['pluginVersion']
        self.plugins = clientInfo['plugins'] #dict
        self.userId = clientInfo['userId']
        self.taskId = clientInfo['taskId']     
        self.Base = PluginBase()
        self._PluginDir = os.path.join(self.Base.get_json_ini('Node_D'),'GolaemCrowd','software',self.cgName + self.cgVersion + '_' + self.pluginName + self.pluginVersion).replace('\\','/')
        self.MyLog(self._PluginDir)
                
    def MyLog(self,message,extr="GolaemCrowdSetup"):      
        if str(message).strip() != "":
            print("[%s] %s"%(extr,str(message)))


    def reCreateMod(self):
        #D盘mod文件夹路径
        MODULES_LOCAL =  self._PluginDir  + r"/Golaem_init/Golaem-%s-Maya%s"%(self.pluginVersion,self.cgVersion)
        if not os.path.exists(MODULES_LOCAL):
            os.makedirs(MODULES_LOCAL)
        #D盘mod文件路径
        module_file = self._PluginDir  + r"/Golaem_init/Golaem-%s-Maya%s/glmCrowd.mod"%(self.pluginVersion,self.cgVersion)
        #专门存放mod的路径
        NEW_MODULE_FILE = self._PluginDir  +r"/Golaem_module/glmCrowd.mod"
        #拷贝mod
        if os.path.exists(module_file):
            shutil.copy(module_file,NEW_MODULE_FILE) 
        #修改mod文件,只修改第一行
        if os.path.exists(module_file):
            fp = open(module_file,'r')
            lines = fp.readlines()
            fp.close()
            lines[0] = "+ glmCrowd %s %s \n"%(self.pluginVersion,NEW_MODULE_FILE)
            fp = open(NEW_MODULE_FILE,'r+')
            for s in lines:
                fp.writelines(s)
            fp.close() 


    def setEnv(self):
        #获取破解文件夹
        AMPED_path = self._PluginDir + r"/Golaem_room/Golaem"
        if os.path.exists(AMPED_path):
            #结束进程,拷贝破解文件夹到C盘及启动rlm
            os.system(r'wmic process where name="rlm_golaem.exe" delete')
            dstDir=r'"C:\Golaem"'
            os.system ("robocopy /e /ns /nc /nfl /ndl /np  %s %s" % (AMPED_path, dstDir))
            os.system(r'start C:\Golaem\rlm_golaem.exe')
        #设置lic环境变量
        _golaem_LICENSE = os.environ.get('golaem_LICENSE ')
        os.environ['golaem_LICENSE'] = (_golaem_LICENSE + r";" if _golaem_LICENSE else "") + r'5053@127.0.0.1'
        self.MyLog("Golaem license local :" + os.environ['golaem_LICENSE'] )
        
        #设置其他变量
        _MAYA_MODULE_PATH = os.environ.get('MAYA_MODULE_PATH')
        os.environ['MAYA_MODULE_PATH'] = (_MAYA_MODULE_PATH + r";" if _MAYA_MODULE_PATH else "") + self._PluginDir + r"/Golaem_module"


        print os.environ.get('MAYA_MODULE_PATH')
        print("\n")
        
        pluginList = clientInfo['plugins']
        if pluginList:
            if 'mtoa' in pluginList:
                _ARNOLD_PROCEDURAL_PATH = os.os.environ.get("ARNOLD_PROCEDURAL_PATH")
                _ARNOLD_PLUGIN_PATH = os.os.environ.get("ARNOLD_PLUGIN_PATH")
                
                os.environ['ARNOLD_PROCEDURAL_PATH'] = (_ARNOLD_PROCEDURAL_PATH + r";" if _ARNOLD_PROCEDURAL_PATH else "") + self._PluginDir + r"/Golaem_init/Golaem-%s-Maya%s/procedurals" % (self.cgVersion,self.pluginVersion)
                os.environ['ARNOLD_PLUGIN_PATH'] = (_ARNOLD_PLUGIN_PATH + r";" if _ARNOLD_PLUGIN_PATH else "") + self._PluginDir + r"/Golaem_init/Golaem-%s-Maya%s/shaders" % (self.cgVersion,self.pluginVersion)

            if 'vrayformaya' in pluginList:
                    if self.cgVersion == "2016.5":
                        maya_ver = "2016_5"
                    else:
                        maya_ver = self.cgVersion
                    
                VRAY_FOR_MAYA_PLUGINS_x64 = "VRAY_FOR_MAYA%s_PLUGINS_x64" % (maya_ver)
                _VRAY_FOR_MAYA_PLUGINS_x64 = os.os.environ.get("VRAY_FOR_MAYA_PLUGINS_x64")
                _VRAY_FOR_MAYA_SHADERS = os.os.environ.get("VRAY_FOR_MAYA_SHADERS")
                
                os.environ['VRAY_FOR_MAYA_PLUGINS_x64'] = (_VRAY_FOR_MAYA_PLUGINS_x64 + r";" if _VRAY_FOR_MAYA_PLUGINS_x64 else "") + self._PluginDir + r"/Golaem_init/Golaem-%s-Maya%s/procedurals" % (self.cgVersion,self.pluginVersion)
                os.environ['VRAY_FOR_MAYA_SHADERS'] = (_VRAY_FOR_MAYA_SHADERS + r";" if _VRAY_FOR_MAYA_SHADERS else "") + self._PluginDir + r"/Golaem_init/Golaem-%s-Maya%s/shaders" % (self.cgVersion,self.pluginVersion)

def main(*args):
    infoDict = args[0]
    configPlugin = GolaemCrowdConfig(infoDict)
    configPlugin.reCreateMod()
    configPlugin.setEnv()
    configPlugin.MyLog( "set GolaemCrowd env finish")


if __name__ == '__main__':
    main()
    # os.system ("\""+MAYA_ROOT + "/bin/maya.exe"+"\"")