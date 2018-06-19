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

class AlShadersConfig():
    def __init__(self,clientInfo):
        # self.MyLog(clientInfo)
        #获取流程脚本传过来的信息
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
        self._PluginDir = os.path.join(self.Base.get_json_ini('Node_D'),'alShaders','software', self.cgName + self.cgVersion + '_' + self.pluginName + self.pluginVersion).replace('\\','/')
        self.MyLog(self._PluginDir)
                
    def MyLog(self,message,extr="AlShadersSetup"):      
        if str(message).strip() != "":
            print("[%s] %s"%(extr,str(message)))


    def EnvSetup(self):
        #设置环境变量
        _ARNOLD_PLUGIN_PATH=os.environ.get('ARNOLD_PLUGIN_PATH')
        _MTOA_TEMPLATES_PATH=os.environ.get('MTOA_TEMPLATES_PATH')
        os.environ['ARNOLD_PLUGIN_PATH'] = (_ARNOLD_PLUGIN_PATH + r";" if _ARNOLD_PLUGIN_PATH else "") + self._PluginDir + r"/bin"
        os.environ['MTOA_TEMPLATES_PATH'] = (_MTOA_TEMPLATES_PATH + r";" if _MTOA_TEMPLATES_PATH else "") + self._PluginDir + r"/ae"
        
        #如果此版本有aexml文件夹 添加多一条环境变量
        aexml_path = self._PluginDir + r"/aexml"
        if os.path.exists(aexml_path):
            print "This alshder version has aexml_path"
            _MAYA_CUSTOM_TEMPLATE_PATH=os.environ.get('MAYA_CUSTOM_TEMPLATE_PATH') 
            os.environ['MAYA_CUSTOM_TEMPLATE_PATH'] = (_MAYA_CUSTOM_TEMPLATE_PATH + r";" if _MAYA_CUSTOM_TEMPLATE_PATH else "") + self._PluginDir + r"/aexml"
        print "set alShaders finished!!!"


def main(*args):
    infoDict = args[0]
    configPlugin = AlShadersConfig(infoDict)
    configPlugin.EnvSetup()
    configPlugin.MyLog( "set alShaders env finish")

if __name__ == '__main__':
    main()
    # os.system ("\""+MAYA_ROOT + "/bin/maya.exe"+"\"")