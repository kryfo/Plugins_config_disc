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


class RealflowConfig():
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
        self._PluginDir = os.path.join(self.Base.get_json_ini('Node_D'),self.pluginName,'software',self.cgName + self.cgVersion + '_' + self.pluginName + self.pluginVersion).replace('\\','/')
        self.mentalrayForMayaVersion= "/mentalrayForMaya%s" % (self.cgVersion )
        self.MyLog(self._PluginDir)

    def MyLog(self,message,extr="RealflowSetup"):      
        if str(message).strip() != "":
            print("[%s] %s"%(extr,str(message)))

    def setEnv(self):        
        #设置环境变量
        _XBMLANGPATH = os.environ.get('XBMLANGPATH')
        os.environ['XBMLANGPATH'] = (_XBMLANGPATH + r";" if _XBMLANGPATH else "") + self._PluginDir + r"/maya_root/icons"
        _MAYA_PLUG_IN_PATH  = os.environ.get('MAYA_PLUG_IN_PATH')
        os.environ['MAYA_PLUG_IN_PATH'] = (_MAYA_PLUG_IN_PATH + r";" if _MAYA_PLUG_IN_PATH else "") + self._PluginDir + r"/maya_root/bin/plug-ins"
        _MAYA_SCRIPT_PATH = os.environ.get('MAYA_SCRIPT_PATH')
        os.environ['MAYA_SCRIPT_PATH'] = (_MAYA_SCRIPT_PATH + r";" if _MAYA_SCRIPT_PATH else "") + self._PluginDir + r"/maya_root/scripts"
        _mentalray_EXTENSIONS_PATH = os.environ.get('mentalray_EXTENSIONS_PATH')
        os.environ['mentalray_EXTENSIONS_PATH'] = (_mentalray_EXTENSIONS_PATH + r";" if _mentalray_EXTENSIONS_PATH else "") + self._PluginDir + self.mentalrayForMayaVersion +r"/shaders"

        
def main(*args):
    infoDict = args[0]
    configPlugin = RealflowConfig(infoDict)
    configPlugin.setEnv()
    configPlugin.MyLog( "set Realflow env finish")
 

if __name__ == '__main__':
    main()
    # os.system ("\""+MAYA_ROOT + "/bin/maya.exe"+"\"")