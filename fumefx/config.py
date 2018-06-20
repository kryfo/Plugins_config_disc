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


class FumefxConfig():
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
        self._PluginDir = os.path.join(self.Base.get_json_ini('Node_D'),'fumefx','software',self.cgName + self.cgVersion + '_' + self.pluginName + self.pluginVersion).replace('\\','/')
        self.MyLog(self._PluginDir)
                
    def MyLog(self,message,extr="FumefxSetup"):      
        if str(message).strip() != "":
            print("[%s] %s"%(extr,str(message)))

    def reCreateMod(self):
        DOME_ROOT_DIR = self._PluginDir
        MODULES_LOCAL = self._PluginDir +r"/maya_root/modules"
        FUMEFX_ROOT = self._PluginDir +r"/maya_fumefx"
        FUMEFX_ROOT_lOCAL = FUMEFX_ROOT.replace("/","\\")
        #获取mod文件,并修改
        MODULE_NAME = "FumeFX.mod"
        NEW_MODULE_FILE = MODULES_LOCAL + r"/" + MODULE_NAME
        line= "+ FumeFX %s %s"%(self.pluginVersion,FUMEFX_ROOT_lOCAL)
        if os.path.exists(NEW_MODULE_FILE):
            fp = open(NEW_MODULE_FILE,'w')
            fp.writelines(line)  
            fp.write('\n')  
            fp.close() 
        else:
            print ("\n module file don't exist: \n" + elm)



    def EnvSetup(self):
    #run rlm >>>>>>>>>>>
        #检测进程并删除
        os.system(r'wmic process where name="AfterFLICS.exe" delete')
        #拷贝rlm文件到C盘
        AFLICS_PATH = self._PluginDir + r"\AFLICS"  
        dstDir=r'"C:\Program Files (x86)\AFLICS"'  
        os.system ("robocopy /e /ns /nc /nfl /ndl /np  %s %s" % (AFLICS_PATH, dstDir))
        #添加服务
        os.system(r'sc create "AfterFLICS V3" binPath= "C:\Program Files (x86)\AFLICS\AfterFLICS.exe"  DisplayName= "AfterFLICS V3"')
        #开启服务
        os.system(r'net start "AfterFLICS V3"')
        self.MyLog("FumeFX server :" + dstDir )
        
        #设置环境变量
        _PATH_ENV = os.environ.get('PATH')
        os.environ['PATH'] =  (_PATH_ENV + r";" if _PATH_ENV else "") + self._PluginDir + r"/maya_root/bin"
        # get maya env
        _MAYA_MODULE_PATH = os.environ.get('MAYA_MODULE_PATH')
        _MAYA_SCRIPT_PATH = os.environ.get('MAYA_SCRIPT_PATH')

        # get mr env
        _MI_LIBRARY_PATH = os.environ.get('MI_LIBRARY_PATH')
        _MI_CUSTOM_SHADER_PATH = os.environ.get('MI_CUSTOM_SHADER_PATH')
        _MENTALRAY_SHADERS_LOCATION = os.environ.get('MENTALRAY_SHADERS_LOCATION')
        _MENTALRAY_INCLUDE_LOCATION = os.environ.get('MENTALRAY_INCLUDE_LOCATION')
        # set maya env
        os.environ['MAYA_MODULE_PATH'] = (_MAYA_MODULE_PATH + r";" if _MAYA_MODULE_PATH else "") + self._PluginDir + r"/maya_root/modules"
        os.environ['MAYA_SCRIPT_PATH'] = (_MAYA_SCRIPT_PATH + r";" if _MAYA_SCRIPT_PATH else "") + self._PluginDir + r"/maya_root/scripts"
        #set mr env
        os.environ['MI_LIBRARY_PATH'] = (_MI_LIBRARY_PATH + r";" if _MI_LIBRARY_PATH else "") + self._PluginDir + r"/mentalray_shader/shaders"
        os.environ['MI_CUSTOM_SHADER_PATH'] = (_MI_CUSTOM_SHADER_PATH + r";" if _MI_CUSTOM_SHADER_PATH else "") + self._PluginDir+ r"/mentalray_shader/shaders/include"
        os.environ['MENTALRAY_SHADERS_LOCATION'] = (_MENTALRAY_SHADERS_LOCATION + r";" if _MENTALRAY_SHADERS_LOCATION else "") + os.environ.get('MI_LIBRARY_PATH')
        os.environ['MENTALRAY_INCLUDE_LOCATION'] = (_MENTALRAY_INCLUDE_LOCATION + r";" if _MENTALRAY_INCLUDE_LOCATION else "") + os.environ.get('MI_CUSTOM_SHADER_PATH')

    #set others plugins's env >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        pluginList = self.plugins
        if pluginList:
            if 'mtoa' in pluginList:
                _ARNOLD_PLUGIN_PATH = os.environ.get('ARNOLD_PLUGIN_PATH ')
                _MTOA_EXTENSIONS_PATH = os.environ.get('MTOA_EXTENSIONS_PATH')

                os.environ['ARNOLD_PLUGIN_PATH'] = (_ARNOLD_PLUGIN_PATH + r";" if _ARNOLD_PLUGIN_PATH else "") + self._PluginDir + r"/arnold_shader/shaders"
                os.environ['MTOA_EXTENSIONS_PATH'] = (_MTOA_EXTENSIONS_PATH + r";" if _MTOA_EXTENSIONS_PATH else "") + self._PluginDir + r'/arnold_shader/extensions'
                print ("arnold and Domemaster3D env set finish!!!") 

            if 'vrayformaya' in pluginList:
                if clientInfo['plugins']["vrayformaya"] == "2016.5":
                    maya_ver = "2016_5"
                else:
                    maya_ver = clientInfo['plugins']["vrayformaya"]
                VRAY_FOR_MAYA_PLUGINS = "VRAY_FOR_MAYA%s_PLUGINS_x64"%(maya_ver)
                
                _VRAY_FOR_MAYA_PLUGINS = os.environ.get('VRAY_FOR_MAYA_PLUGINS ')
                _VRAY_FOR_MAYA_SHADERS = os.environ.get('VRAY_FOR_MAYA_SHADERS ')

                os.environ['VRAY_FOR_MAYA_PLUGINS'] = (_VRAY_FOR_MAYA_PLUGINS + r";" if _VRAY_FOR_MAYA_PLUGINS else "") + self._PluginDir + r"/vray3.0_shader/vrayplugins"
                os.environ['VRAY_FOR_MAYA_SHADERS'] = (_VRAY_FOR_MAYA_SHADERS + r";" if _VRAY_FOR_MAYA_SHADERS else "") + self._PluginDir + r"/vray3.0_shader/shaders"
                print ("vrayformaya and Domemaster3D env set finish!!!") 


def main(*args):
    infoDict = args[0]
    configPlugin = FumefxConfig(infoDict)
    #修改mod
    configPlugin.reCreateMod()
    #拷贝服务文件到C盘,并启动,设置环境变量
    configPlugin.EnvSetup()
    configPlugin.MyLog( "set Fumefx env finish")



if __name__ == '__main__':
    main()
    # os.system ("\""+MAYA_ROOT + "/bin/maya.exe"+"\"")