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


class PgYetiConfig():
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
        self._PluginDir = os.path.join(self.Base.get_json_ini('Node_D'),self.pluginName,'software',self.cgName + self.cgVersion + '_' + self.pluginName + self.pluginVersion).replace('\\','/')
        #vray的插件变量名称
        self.VRAY_FOR_MAYA_VERSION_PLUGINS_x64 = "VRAY_FOR_MAYA%s_PLUGINS_x64" % (self.cgVersion )
        #获取lic码
        self.PEREGRINEL_LICENSE = self.Base.get_json_ini('PEREGRINEL_LICENSE')
        #如果存在rlm文件夹   则不采用公共lic码  获取 rlm文件夹内的lic
        if os.path.exists(os.path.join(self._PluginDir,'rlm')):  
            local_lic1 = os.path.normpath(os.path.join(self._PluginDir,'rlm','peregrinel.lic'))
            local_lic2 = os.path.normpath(os.path.join(self._PluginDir,'rlm','yeti.lic'))
            self.PEREGRINEL_LICENSE = local_lic1 + ";" + local_lic2 + ";" + self.PEREGRINEL_LICENSE 
        #yeti的临时缓存路径   "D:/temp/MAYA/yetiCache"  
        self.YETI_TMP = self.Base.get_json_ini('YETI_TMP')
        self.MyLog(self._PluginDir)

    def MyLog(self,message,extr="PgYetiSetup"):      
        if str(message).strip() != "":
            print("[%s] %s"%(extr,str(message)))

    def reCreateMod(self):
        #获取mod路径
        MODULES_LOCAL =  self._PluginDir  + r"/maya_root/modules/"
        if not os.path.exists(MODULES_LOCAL):
            os.makedirs(MODULES_LOCAL)
        module_file = self._PluginDir  + r"/maya_root/modules/pgYetiMaya.mod"
        #设置mod内容
        NEW_MAYAM_MTOA_PATH = self._PluginDir + r"/maya_yeti"
        ModulePathList = []
        line1 = "+ pgYetiMaya " + self.pluginVersion + " "  + NEW_MAYAM_MTOA_PATH
        line2 = "PATH +:= bin"
        line3 = "MTOA_EXTENSIONS_PATH +:= plug-ins"
        line4 = "ARNOLD_PLUGIN_PATH +:= bin"
        line5 = "VRAY_FOR_MAYA2017_PLUGINS_x64 +:= bin"
        ModulePathList = [line1,line2,line3,line4,line5]
        if os.path.exists(module_file):
            fp = open(module_file,'w')
            for line in ModulePathList:
                fp.writelines(line)  
                fp.write('\n')  
            fp.close() 


    def setEnv(self):        
        if not os.path.exists(self.YETI_TMP):
            os.makedirs(self.YETI_TMP)
        #添加环境变量
        os.environ['YETI_TMP'] = self.YETI_TMP      
        os.environ['PEREGRINEL_LICENSE'] = self.PEREGRINEL_LICENSE

        self.MyLog("pgYeti license local :" + os.environ['PEREGRINEL_LICENSE'] )
        # _PATH_env=os.environ.get('PATH')
        _MAYA_MODULE_PATH=os.environ.get('MAYA_MODULE_PATH')
        # os.environ['PATH'] = (_PATH_env + r";" if _PATH_env else "") + self._PluginDir  + r'/maya_yeti/bin' 
        os.environ['MAYA_MODULE_PATH'] = (_MAYA_MODULE_PATH + r";" if _MAYA_MODULE_PATH else "") + self._PluginDir + r"/maya_root/modules"
        
        if 'PATH' not in os.environ:
            os.environ['PATH'] = self._PluginDir + r'\maya_yeti\bin'
        else:
            os.environ['PATH'] = os.environ.get('PATH') + r';'+ self._PluginDir + r'\maya_yeti\bin'

        #print("shaveNode " + pluginList[shaveNode] + " setting done!")
        if self.plugins:
            #设置扩展包路径与程序包路径
            if 'mtoa' in self.plugins:
                if 'MTOA_EXTENSIONS_PATH' not in os.environ:
                    os.environ['MTOA_EXTENSIONS_PATH'] = self._PluginDir + r"\maya_yeti\plug-ins"
                else:
                    os.environ['MTOA_EXTENSIONS_PATH'] = os.environ.get('MTOA_EXTENSIONS_PATH') + r';' + self._PluginDir + r'\maya_yeti\plug-ins'
                if 'MTOA_PROCEDURAL_PATH' not in os.environ:
                    os.environ['MTOA_PROCEDURAL_PATH'] = self._PluginDir + r"\maya_yeti\bin"
                else:
                    os.environ['MTOA_PROCEDURAL_PATH'] = os.environ.get('MTOA_PROCEDURAL_PATH') + r';' + self._PluginDir + r'\maya_yeti\bin'
            
            if 'vrayformaya' in self.plugins:
                if self.VRAY_FOR_MAYA_VERSION_PLUGINS_x64 not in os.environ:
                    os.environ[self.VRAY_FOR_MAYA_VERSION_PLUGINS_x64] = self._PluginDir + r"\maya_yeti\bin"
                else:
                    os.environ[self.VRAY_FOR_MAYA_VERSION_PLUGINS_x64] = os.environ.get(self.VRAY_FOR_MAYA_VERSION_PLUGINS_x64) + r';' + self._PluginDir + r"\maya_yeti\bin"
                if 'VRAY_PLUGINS_x64' not in os.environ:
                    os.environ['VRAY_PLUGINS_x64'] = self._PluginDir + r"\maya_yeti\bin"
                else:
                    os.environ['VRAY_PLUGINS_x64'] = os.environ.get('VRAY_PLUGINS_x64') + r';' + self._PluginDir + r'\maya_yeti\bin'
            
            if 'redshift_GPU' in self.plugins:
                if 'REDSHIFT_MAYAEXTENSIONSPATH' not in os.environ:
                    os.environ['REDSHIFT_MAYAEXTENSIONSPATH'] = self._PluginDir + r"\maya_yeti\plug-ins"
                else:
                    os.environ['REDSHIFT_MAYAEXTENSIONSPATH'] = os.environ.get('REDSHIFT_MAYAEXTENSIONSPATH') + r';' + self._PluginDir + r"\maya_yeti\plug-ins"
            
            if 'RenderMan_for_Maya' in self.plugins:            
                os.environ['YETI_HOME'] = self._PluginDir + r"\maya_yeti"
                os.environ['RMS_SCRIPT_PATHS'] = self._PluginDir + r"\RMS_SCRIPT_PATHS"
                

        
def main(*args):
    infoDict = args[0]
    configPlugin = PgYetiConfig(infoDict)
    configPlugin.reCreateMod()
    configPlugin.setEnv()
    configPlugin.MyLog( "set pgYetiMaya env finish")
 

if __name__ == '__main__':
    main()
    # os.system ("\""+MAYA_ROOT + "/bin/maya.exe"+"\"")