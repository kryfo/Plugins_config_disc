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


class ShaveNodeConfig():
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
        #D盘插件路径
        self._PluginDir = os.path.join(self.Base.get_json_ini('Node_D'),self.pluginName,'software',self.cgName + self.cgVersion + '_' + self.pluginName + self.pluginVersion).replace('\\','/')
        #获取变量名称
        self.VRAY_FOR_MAYA_VERSION_PLUGINS_x64 = "VRAY_FOR_MAYA%s_PLUGINS_x64" % (self.cgVersion )
        self.mentalrayForMayaVersion= "/mentalrayForMaya%s" % (self.cgVersion )
        self.MyLog(self._PluginDir)

    def MyLog(self,message,extr="shaveNodeSetup"):      
        if str(message).strip() != "":
            print("[%s] %s"%(extr,str(message)))

    def reCreateMod(self):
        MODULES_LOCAL =  self._PluginDir  + r"/maya_root/modules/"
        if not os.path.exists(MODULES_LOCAL):
            os.makedirs(MODULES_LOCAL)
        module_file = self._PluginDir  + r"/maya_root/modules/shaveHaircut.mod"
        #修改mod文件
        NEW_MAYAM_MTOA_PATH = self._PluginDir + r"/maya_shave"
        ModulePathList = []
        line1 = "+ shaveHaircut 1.1 " + NEW_MAYAM_MTOA_PATH
        ModulePathList = [line1]
        if os.path.exists(module_file):
            fp = open(module_file,'w')
            for line in ModulePathList:
                fp.writelines(line)  
                fp.write('\n')  
            fp.close() 


    def setEnv(self):
        #拷贝压缩包内的rlm到C盘
        srcRlmDir= self._PluginDir + r"\rlm"
        dstRlmDir=r"C:\rlm"
        os.system ("robocopy /e /ns /nc /nfl /ndl /np  %s %s" % (srcRlmDir, dstRlmDir))

        #拷贝lic文件夹到C盘 开启rlm
        RLMServer_path= self._PluginDir + r"\RLMServer"
        self.MyLog(RLMServer_path)
        if os.path.exists(RLMServer_path):
            srcRlmDir= self._PluginDir + r"\RLMServer"
            dstRlmDir=r"C:\RLMServer"
            os.system ("robocopy /e /ns /nc /nfl /ndl /np  %s %s" % (srcRlmDir, dstRlmDir))
            #开启rlm
            os.system(r'start C:\RLMServer\rlm_shave.exe')

        #设置lic环境变量
        if not os.environ.has_key('RLM_LICENSE'):
            os.environ['RLM_LICENSE'] ="5077@127.0.0.1"
        else:
            os.environ['RLM_LICENSE'] = os.environ.get('RLM_LICENSE') + r';'+"5077@127.0.0.1"
            self.MyLog("9.5v9 license")

        _PATH_ENV = os.environ.get('PATH')
        _MAYA_PLUG_IN_PATH  = os.environ.get('MAYA_PLUG_IN_PATH')
        _MAYA_SCRIPT_PATH = os.environ.get('MAYA_SCRIPT_PATH ')
        _MAYA_MODULE_PATH = os.environ.get('MAYA_MODULE_PATH')
        _XBMLANGPATH = os.environ.get('XBMLANGPATH')

        #添加其余环境变量
        os.environ['XBMLANGPATH'] = (_XBMLANGPATH + r";" if _XBMLANGPATH else "") + self._PluginDir + r"/maya_root/icons"
        os.environ['PATH'] = (_PATH_ENV + r";" if _PATH_ENV else "") + self._PluginDir + r"/maya_root/bin"
        os.environ['MAYA_PLUG_IN_PATH'] = (_MAYA_PLUG_IN_PATH + r";" if _MAYA_PLUG_IN_PATH else "") + self._PluginDir + r"/maya_shave/plug-ins"
        os.environ['MAYA_SCRIPT_PATH'] = (_MAYA_SCRIPT_PATH + r";" if _MAYA_SCRIPT_PATH else "") + self._PluginDir + r"/maya_shave/scripts"
        os.environ['MAYA_MODULE_PATH'] = (_MAYA_MODULE_PATH + r";" if _MAYA_MODULE_PATH else "") + self._PluginDir + r"/maya_root/modules"
        #以下这条多余
        _XBMLANGPATH = os.environ.get('XBMLANGPATH')
        os.environ['XBMLANGPATH'] = (_XBMLANGPATH + r";" if _XBMLANGPATH else "") + self._PluginDir + r"/maya_root/icons"
        
        _mentalray_EXTENSIONS_PATH = os.environ.get('mentalray_EXTENSIONS_PATH')
        os.environ['mentalray_EXTENSIONS_PATH'] = (_mentalray_EXTENSIONS_PATH + r";" if _mentalray_EXTENSIONS_PATH else "") + self._PluginDir + self.mentalrayForMayaVersion +r"/shaders"

        if self.plugins:
            if 'vrayformaya' in self.plugins:
                if self.VRAY_FOR_MAYA_VERSION_PLUGINS_x64 not in os.environ:
                    os.environ[self.VRAY_FOR_MAYA_VERSION_PLUGINS_x64] = self._PluginDir + r"\maya_yeti\bin"
                else:
                    os.environ[self.VRAY_FOR_MAYA_VERSION_PLUGINS_x64] = os.environ.get(self.VRAY_FOR_MAYA_VERSION_PLUGINS_x64) + r';' + self._PluginDir + r"\maya_yeti\bin"
                if 'VRAY_PLUGINS_x64' not in os.environ:
                    os.environ['VRAY_PLUGINS_x64'] = self._PluginDir + r"\maya_yeti\bin"
                else:
                    os.environ['VRAY_PLUGINS_x64'] = os.environ.get('VRAY_PLUGINS_x64') + r';' + self._PluginDir + r'\maya_yeti\bin'

    def CopyExtfile(self):
        D_ROOT = self.Base.get_json_ini('Node_D')
        EXT_ROOT = self.Base.get_json_ini('MAYA_Plugin_Dir')
        if self.plugins:
            if "mtoa" in self.plugins:
                self.MyLog("<<<<<<Set arnold for shaveNode Extension file>>>>>>>")
                ARNOLD_VERSION = self.plugins['mtoa']
                #获取arnold路径
                ARNOLD_PATH = D_ROOT + r"/mtoa/software/maya%s_mtoa%s" % (self.cgVersion,ARNOLD_VERSION)
                extlist = ["2.0.1"]
                #获取扩展包路径
                if ARNOLD_VERSION in extlist:

                    EXT_SHADERS = EXT_ROOT + r"/shaveNode/extensions_for_Mtoa/maya%s_mtoa%s/shaders" % (self.cgVersion,ARNOLD_VERSION)
                    EXT_FILE = EXT_ROOT + r"/shaveNode/extensions_for_Mtoa/maya%s_mtoa%s/extensions" % (self.cgVersion,ARNOLD_VERSION)
                else:
                    extlist.sort()
                    ext_ver = extlist[-1]
                    EXT_SHADERS = EXT_ROOT + r"/shaveNode/extensions_for_Mtoa/maya%s_mtoa%s/shaders" % (self.cgVersion,ext_ver)
                    EXT_FILE = EXT_ROOT + r"/shaveNode/extensions_for_Mtoa/maya%s_mtoa%s/extensions" % (self.cgVersion,ext_ver)
                
                if not (os.path.exists(EXT_SHADERS) and os.path.exists(EXT_FILE)):
                    self.MyLog("Current this arnold or maya version don't have shave extsiontion file in B disk,please offer your own file....")
                
                #拷贝扩展包路径
                if not (os.path.exists(ARNOLD_PATH + r"/maya_mtoa/shaders/shave_shaders.dll") and os.path.exists(ARNOLD_PATH + r"/maya_mtoa/extensions/shave.dll") and os.path.exists(ARNOLD_PATH + r"/maya_mtoa/extensions/shave.py")):
                    Shaders_srcDir = EXT_SHADERS
                    Shaders_dstDir = ARNOLD_PATH + r"/maya_mtoa/shaders"
                    os.system ("robocopy /s  %s %s" % (Shaders_srcDir, Shaders_dstDir))
                    
                    Ext_srcDir = EXT_FILE
                    Ext_dstDir = ARNOLD_PATH + r"/maya_mtoa/extensions"
                    os.system ("robocopy /s  %s %s" % (Ext_srcDir, Ext_dstDir))
                else:
                    self.MyLog("This arnold vesion already has the shave extension file ")
                    
                self.MyLog("<<<<<<<Set arnold for shaveNode Extension file env finsh!!!>>>>>>>")

        
def main(*args):
    infoDict = args[0]
    #获取信息
    configPlugin = ShaveNodeConfig(infoDict)
    #修改mod文件
    configPlugin.reCreateMod()
    #设置环境变量,拷贝rlm,启动rlm
    configPlugin.setEnv()
    #获取B盘扩展包路径并拷贝到D盘
    configPlugin.CopyExtfile()
    configPlugin.MyLog( "set shaveNode env finish")
 

if __name__ == '__main__':
    main()
    # os.system ("/""+MAYA_ROOT + "/bin/maya.exe"+"\"")