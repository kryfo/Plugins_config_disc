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


class MtoaConfig():
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
        self._PluginDir = os.path.join(self.Base.get_json_ini('Node_D'),self.pluginName,'software',self.cgName + self.cgVersion + '_' + self.pluginName + self.pluginVersion).replace('\\','/')
        #"solidangle_LICENSE":"5060@127.0.0.1;5060@10.60.96.203;5060@10.60.5.248"
        self.solidangle_LICENSE = self.Base.get_json_ini('solidangle_LICENSE')
        self.MyLog(self._PluginDir)
                
    def MyLog(self,message,extr="MtoaSetup"):      
        if str(message).strip() != "":
            print("[%s] %s"%(extr,str(message)))

    #修改或创建 mod文件
    def reCreateMod(self):
        #本地modules路径
        MODULES_LOCAL =  self._PluginDir  + r"/maya_root/modules"
        if not os.path.exists(MODULES_LOCAL):
            os.makedirs(MODULES_LOCAL)
        #本地mod文件路径
        module_file = self._PluginDir  + r"/maya_root/modules/mtoa.mod"
        NEW_MAYAM_MTOA_PATH = self._PluginDir  +r"/maya_mtoa"
        #mod文件的内容
        ModulePathList = []
        line1 = "+ mtoa any " + NEW_MAYAM_MTOA_PATH
        line2 = "PATH +:= bin"
        line3 = "MAYA_CUSTOM_TEMPLATE_PATH +:= scripts/mtoa/ui/templates"
        line4 = "MAYA_SCRIPT_PATH +:= scripts/mtoa/mel"
        ModulePathList = [line1,line2,line3,line4]
        #写入内容
        if os.path.exists(module_file):
            fp = open(module_file,'w')
            for line in ModulePathList:
                fp.writelines(line)  
                fp.write('\n')  
            fp.close() 

        #拷贝xml到 rendererDesc文件夹
        ORG_DESCRIPT_FILE = NEW_MAYAM_MTOA_PATH + r"/arnoldRenderer.xml"
        NEW_DESCRIPT_DIR = self._PluginDir  + r"/maya_root/bin/rendererDesc"
        if not os.path.exists(NEW_DESCRIPT_DIR):
            os.makedirs(NEW_DESCRIPT_DIR)
        shutil.copy(ORG_DESCRIPT_FILE,NEW_DESCRIPT_DIR) 

    #结束lic相关进程,设置环境变量 启动进程
    def setEnv(self):
        AMPED_path = self._PluginDir + r"/AMPED"
        if os.path.exists(AMPED_path):
            #结束进程
            os.system(r'wmic process where name="JGS_mtoa_licserver.exe" delete')
            os.system(r'wmic process where name="rlm.exe" delete')
            dstDir=r'"C:\AMPED"'
            #拷贝rlm文件到C盘
            os.system ("robocopy /e /ns /nc /nfl /ndl /np  %s %s" % (AMPED_path, dstDir))
            os.system(r'start C:\AMPED\rlm.exe')
        #设置lic环境变量
        os.environ['solidangle_LICENSE'] = self.solidangle_LICENSE
        self.MyLog("arnold license local :" + os.environ['solidangle_LICENSE'] )

        #设置其他变量
        _PATH_env=os.environ.get('PATH')
        _MAYA_RENDER_DESC_PATH=os.environ.get('MAYA_RENDER_DESC_PATH')
        _MAYA_MODULE_PATH=os.environ.get('MAYA_MODULE_PATH')
        _MAYA_SCRIPT_PATH=os.environ.get('MAYA_SCRIPT_PATH')
        os.environ['PATH'] = (_PATH_env + r";" if _PATH_env else "") + self._PluginDir  + r'/maya_mtoa/bin' 
        os.environ['MAYA_RENDER_DESC_PATH'] = (_MAYA_RENDER_DESC_PATH + r";" if _MAYA_RENDER_DESC_PATH else "") + self._PluginDir + r"/maya_root/bin/rendererDesc"
        os.environ['MAYA_MODULE_PATH'] = (_MAYA_MODULE_PATH + r";" if _MAYA_MODULE_PATH else "") + self._PluginDir + r"/maya_root/modules"
        os.environ['MAYA_SCRIPT_PATH'] = (_MAYA_SCRIPT_PATH + r";" if _MAYA_SCRIPT_PATH else "") + self._PluginDir + r"/maya_mtoa/scripts"    


def main(*args):
    infoDict = args[0]
    configPlugin = MtoaConfig(infoDict)
    configPlugin.reCreateMod()
    configPlugin.setEnv()
    configPlugin.MyLog( "set mtoa env finish")


if __name__ == '__main__':
    main()
    # os.system ("\""+MAYA_ROOT + "/bin/maya.exe"+"\"")