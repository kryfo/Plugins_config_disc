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

class CryptomatteConfig():
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
        self._PluginDir = os.path.join(self.Base.get_json_ini('Node_D'),'Cryptomatte','software',self.cgName + self.cgVersion + '_' + self.pluginName + self.pluginVersion).replace('\\','/')
        self.MyLog(self._PluginDir)
                
    def MyLog(self,message,extr="CryptomatteSetup"):      
        if str(message).strip() != "":
            print("[%s] %s"%(extr,str(message)))

    #设置环境变量
    def EnvSetup(self):
        _ARNOLD_PLUGIN_PATH=os.environ.get('ARNOLD_PLUGIN_PATH')
        _MTOA_TEMPLATES_PATH=os.environ.get('MTOA_TEMPLATES_PATH')
        os.environ['ARNOLD_PLUGIN_PATH'] = (_ARNOLD_PLUGIN_PATH + r";" if _ARNOLD_PLUGIN_PATH else "") + self._PluginDir + r"/bin"
        os.environ['MTOA_TEMPLATES_PATH'] = (_MTOA_TEMPLATES_PATH + r";" if _MTOA_TEMPLATES_PATH else "") + self._PluginDir + r"/ae"
        
        #如果有aexml文件夹  则添加多一条变量
        aexml_path = self._PluginDir + r"/aexml"
        if os.path.exists(aexml_path):
            print "This alshder version has aexml_path"
            _MAYA_CUSTOM_TEMPLATE_PATH=os.environ.get('MAYA_CUSTOM_TEMPLATE_PATH') 
            os.environ['MAYA_CUSTOM_TEMPLATE_PATH'] = (_MAYA_CUSTOM_TEMPLATE_PATH + r";" if _MAYA_CUSTOM_TEMPLATE_PATH else "") + self._PluginDir + r"/aexml"
        print "set Cryptomatte finished!!!"


def main(*args):
    infoDict = args[0]
    configPlugin = CryptomatteConfig(infoDict)
    configPlugin.EnvSetup()
    configPlugin.MyLog( "set Cryptomatte env finish")

if __name__ == '__main__':
    main()
    # os.system ("\""+MAYA_ROOT + "/bin/maya.exe"+"\"")
    # test git
