#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import sys
import os
import shutil
import subprocess
reload(sys)
sys.setdefaultencoding('utf-8')
from MayaPlugin import PluginBase


class RenderManConfig():
    def __init__(self,clientInfo):
        #获取流程脚本传过来的信息
        self.MyLog(clientInfo)
        self.cgName = clientInfo['cgName']
        self.cgVersion = clientInfo['cgVersion']
        self.pluginName = clientInfo['pluginName']
        self.pluginVersion = clientInfo['pluginVersion']
        self.plugins = clientInfo['plugins'] #dict
        self.userId = clientInfo['userId']
        self.taskId = clientInfo['taskId'] 
        #import 公共使用的函数 PluginBase  ，配置脚本（W2        B:/plugins/maya_new/envInfo.json）信息获取，清理目录，创建目录，找相同命名的压缩包，拷贝文件，拷贝目录，解压文件，编码转换，MD5值校验
        self.Base = PluginBase()
        #获取本地文件夹路径
        self._PluginDir = os.path.join(self.Base.get_json_ini('Node_D'),'renderman','software',self.cgName + self.cgVersion + '_' + self.pluginName + self.pluginVersion).replace('\\','/')
        self._PluginLogDir = os.path.join(self.Base.get_json_ini('Node_D'),'renderman','logs').replace('\\','/')
        self.MyLog(self._PluginDir)
                
    def MyLog(self,message,extr="RendermanSetup"):      
        if str(message).strip() != "":
            print("[%s] %s"%(extr,str(message)))


    def reCreateMod(self):
        #获取mod文件,并修改内容
        MODULE_PLG_DIR = self._PluginDir + r"/ETC/RENDERMAN_FOR_MAYA.MODULE"
        MODULE_PLG_CONTENT = "+ RENDERMAN_FOR_MAYA " + self.pluginVersion + " " + self._PluginDir
        with open(MODULE_PLG_DIR, "w") as f:
            f.write(MODULE_PLG_CONTENT)


    def Copyrmps(self):
        #z7路径
        TOOL_DIR = self.Base.get_json_ini('toolDir').replace('\\','/')
        _PATH = os.environ.get('PATH')
        os.environ['PATH'] = (_PATH if _PATH else "") + r";" + TOOL_DIR

        
        #\\10.60.100.151\td\plugins\maya_new\renderman\RenderManProServer
        RMPS_PATH = os.path.join(self.Base.get_json_ini('MAYA_Plugin_Dir'),'renderman','RenderManProServer').replace('\\','/')
        RMPS_FILE = "RenderManProServer" + '_' + self.pluginVersion
        ZIP_FILE = RMPS_FILE + '.7z'
        
        #renderman工具包
        #\\10.60.100.151\td\plugins\maya_new\renderman\RenderManProServer\RenderManProServer_20.4.7z
        SERVER_FILE = os.path.join(self.Base.get_json_ini('MAYA_Plugin_Dir'),'renderman','RenderManProServer',RMPS_FILE + '.7z').replace('\\','/')
        
        self.MyLog("server RenderManProServer  file:" + SERVER_FILE)
        

        LOCAL7Z_PATH =  os.path.join(self.Base.get_json_ini('Node_D'),'renderman','source')
        #D盘插件路径
        LOCAL_ROOT = os.path.join(self.Base.get_json_ini('Node_D'),'renderman','software',RMPS_FILE).replace('\\','/')
        
        #拷贝工具包z7到本地,并解压
        if os.path.exists(SERVER_FILE):
            self.MyLog("Copy RenderManProServer !!!!")
            if not os.path.exists(LOCAL_ROOT):
                os.makedirs()
                
            self.MyLog("RenderManProServer copy : %s/RMPS_COPY.txt" % self._PluginLogDir)
            COPYPRMPS_CMD = "robocopy /S /NDL /NFL %s %s %s" % (RMPS_PATH, LOCAL7Z_PATH,ZIP_FILE)
            LOG_ROOT = open("%s/RMPS_COPY.txt" % self._PluginLogDir ,"wt")
            source_copy = subprocess.Popen(COPYPRMPS_CMD,stdout=LOG_ROOT,shell=True)
            source_copy.wait()
            LOG_ROOT.close()
            
            self.MyLog("RenderManProServer unzip : %s/RMPS_UNZIP.txt" % self._PluginLogDir)
            RMPSUNZIP_CMD = TOOL_DIR + r"/7z.exe x -y -aos " + LOCAL7Z_PATH + r"/" + ZIP_FILE + " -o" + LOCAL_ROOT
            LOG_ROOT = open("%s/RMPS_UNZIP.txt" % self._PluginLogDir ,"wt")
            source_copy = subprocess.Popen(RMPSUNZIP_CMD,stdout=LOG_ROOT,shell=True)
            source_copy.wait()
            LOG_ROOT.close()
            
            # os.system ("robocopy /S /NDL /NFL %s %s %s" % (RMPS_PATH, LOCAL7Z_PATH,ZIP_FILE))
            # subprocess.call(TOOL_DIR + r"/7z.exe x -y -aos " + LOCAL7Z_PATH + r"/" + ZIP_FILE + " -o" + LOCAL_ROOT)
        else:
            self.MyLog("This renderman version dont't has the RenderManProServer file !!!")
            
    def setEnv(self):
        #D:\PLUGINS\MAYA\REDSHIFT\software\maya2017_renderman20.12
        RMS_TREE = self._PluginDir
        #D:\PLUGINS\MAYA\REDSHIFT\software\RenderManProServer_20.12
        RMPS_PATH = os.path.join(self.Base.get_json_ini('Node_D'),'renderman','software',"RenderManProServer" + '_' + self.pluginVersion).replace('\\','/')
        
        __MAYA_MODULE_PATH        = RMS_TREE + r"/etc"
        __MAYA_PLUG_IN_PATH       = RMS_TREE + r"/plug-ins"
        __MAYA_SCRIPT_PATH        = RMS_TREE + r"/scripts" + ";" 
        
        __MAYA_RENDER_DESC_PATH   = RMS_TREE + r"/etc"
        __XBMLANGPATH             = RMS_TREE + r"/icons"
        __PATH                    = RMS_TREE + r"/bin;" +RMPS_PATH+"/bin"

        _MMP  = os.environ.get('MAYA_MODULE_PATH')
        _MPIP = os.environ.get('MAYA_PLUG_IN_PATH')
        _MSP  = os.environ.get('MAYA_SCRIPT_PATH')
        _MRDP = os.environ.get('MAYA_RENDER_DESC_PATH')
        _XBMP = os.environ.get('XBMLANGPATH')
        _PATH = os.environ.get('PATH')
        
        # add to system env
        self.MyLog("Set renderman license !!!")
        #拷贝B盘的lic文件夹到本地D盘
        SERVER_PIXAR_LICENSE_PATH = os.path.join(self.Base.get_json_ini('MAYA_Plugin_Dir'),'renderman','license','locknode').replace('\\','/')
        LOCAL_PIXAR_LICENSE_PATH  = os.path.join(self.Base.get_json_ini('Node_D'),'renderman','license').replace('\\','/')
        LICENSE_NAMEE = "pixar.license"
        LOCAL_lICENSE_FILE = LOCAL_PIXAR_LICENSE_PATH + r'/' + LICENSE_NAMEE
        
        os.system ("robocopy /S /NDL /NFL %s %s %s" % (SERVER_PIXAR_LICENSE_PATH, LOCAL_PIXAR_LICENSE_PATH,LICENSE_NAMEE))
        
        #设置lic的环境变量 
        os.environ['PIXAR_LICENSE_FILE'] = LOCAL_lICENSE_FILE
        
        self.MyLog("RenderMan  license local :" + os.environ['PIXAR_LICENSE_FILE'] )
        
        #设置其余环境变量
        os.environ['RMSTREE']  = RMS_TREE
        os.environ['RMANTREE'] = RMPS_PATH
        os.environ['MAYA_MODULE_PATH']  = (_MMP if _MMP else "") + r";" + __MAYA_MODULE_PATH
        os.environ['MAYA_PLUG_IN_PATH'] = (_MPIP if _MPIP else "") + r";" + __MAYA_PLUG_IN_PATH
        os.environ['MAYA_SCRIPT_PATH']  = (_MSP if _MSP else "") + r";" + __MAYA_SCRIPT_PATH
        os.environ['MAYA_RENDER_DESC_PATH'] = (_MRDP if _MRDP else "") + r";" + __MAYA_RENDER_DESC_PATH
        os.environ['XBMLANGPATH'] = (_XBMP if _XBMP else "") + r";" + __XBMLANGPATH
        os.environ['PATH'] = (_PATH if _PATH else "") + r";" + __PATH 
        
        #以下是废话
        _MMP = os.environ.get('MAYA_MODULE_PATH')
        _MPIP = os.environ.get('MAYA_PLUG_IN_PATH')
        _MSP = os.environ.get('MAYA_SCRIPT_PATH')
        _MRDP = os.environ.get('MAYA_RENDER_DESC_PATH')
        _XBMP = os.environ.get('XBMLANGPATH')
        _PATH = os.environ.get('PATH')
        
def main(*args):
    infoDict = args[0]
    configPlugin = RenderManConfig(infoDict)
    #修改D盘mod文件内容
    configPlugin.reCreateMod()
    #拷贝插件工具包到本地D盘,并解压
    configPlugin.Copyrmps()
    #拷贝lic文件到D盘,设置环境变量
    configPlugin.setEnv()
    configPlugin.MyLog( "set Renderman env finish")


if __name__ == '__main__':
    main()
    # os.system ("\""+MAYA_ROOT + "/bin/maya.exe"+"\"")