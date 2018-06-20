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


class OpenvdbConfig():
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
        
        self.VRAY_FOR_MAYA_VERSION_PLUGINS_x64 = "VRAY_FOR_MAYA%s_PLUGINS_x64" % (self.cgVersion )
        self.PEREGRINEL_LICENSE = self.Base.get_json_ini('PEREGRINEL_LICENSE')
        self.YETI_TMP = self.Base.get_json_ini('YETI_TMP')
        self.MyLog(self._PluginDir)

    def MyLog(self,message,extr="PgYetiSetup"):      
        if str(message).strip() != "":
            print("[%s] %s"%(extr,str(message)))

    #修改mod
    def reCreateMod(self):
        MODULES_LOCAL =  self._PluginDir  + r"/maya_root/modules/"
        if not os.path.exists(MODULES_LOCAL):
            os.makedirs(MODULES_LOCAL)
        #获取mod文件
        module_file = self._PluginDir  + r"/maya_root/modules/openvdb.mod"
        #vbd主路劲
        NEW_MAYAM_MTOA_PATH = self._PluginDir + r"/maya_openvdb"
        self.MyLog(NEW_MAYAM_MTOA_PATH)
        ModulePathList = []
        #修改mod
        line1 = "+ maya%s %s %s" % (self.cgVersion, self.pluginVersion, NEW_MAYAM_MTOA_PATH)
        ModulePathList = [line1]
        if os.path.exists(module_file):
            fp = open(module_file,'w')
            for line in ModulePathList:
                fp.writelines(line)  
                fp.write('\n')  
            fp.close() 

    #设置环境变量
    def setEnv(self):        
        _MAYA_MODULE_PATH = os.environ.get('MAYA_MODULE_PATH')
        _MAYA_PLUG_IN_PATH  = os.environ.get('MAYA_PLUG_IN_PATH')
        _MAYA_SCRIPT_PATH = os.environ.get('MAYA_SCRIPT_PATH ')
        os.environ['MAYA_MODULE_PATH'] = (_MAYA_MODULE_PATH + r";" if _MAYA_MODULE_PATH else "") + self._PluginDir + r"/maya_openvdb/module"
        os.environ['MAYA_PLUG_IN_PATH'] = (_MAYA_PLUG_IN_PATH + r";" if _MAYA_PLUG_IN_PATH else "") + self._PluginDir + r"/maya_openvdb/plug-ins"
        os.environ['MAYA_SCRIPT_PATH'] = (_MAYA_SCRIPT_PATH + r";" if _MAYA_SCRIPT_PATH else "") + self._PluginDir + r"/maya_openvdb/scripts"
        # if self.plugins:
            # if 'mtoa' in self.plugins:
                # if 'MTOA_EXTENSIONS_PATH' not in os.environ:
                    # os.environ['MTOA_EXTENSIONS_PATH'] = self._PluginDir + r"\maya_yeti\plug-ins"
                # else:
                    # os.environ['MTOA_EXTENSIONS_PATH'] = os.environ.get('MTOA_EXTENSIONS_PATH') + r';' + self._PluginDir + r'\maya_yeti\plug-ins'
                # if 'MTOA_PROCEDURAL_PATH' not in os.environ:
                    # os.environ['MTOA_PROCEDURAL_PATH'] = self._PluginDir + r"\maya_yeti\bin"
                # else:
                    # os.environ['MTOA_PROCEDURAL_PATH'] = os.environ.get('MTOA_PROCEDURAL_PATH') + r';' + self._PluginDir + r'\maya_yeti\bin'


        
def main(*args):
    infoDict = args[0]
    configPlugin = OpenvdbConfig(infoDict)
    #修改mod
    configPlugin.reCreateMod()
    #设置环境变量
    configPlugin.setEnv()
    configPlugin.MyLog( "set pgYetiMaya env finish")
 

if __name__ == '__main__':
    main()
    # os.system ("\""+MAYA_ROOT + "/bin/maya.exe"+"\"")