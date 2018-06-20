'''
Creat 
'''
import os,sys
import subprocess
import re,time

class PlugPlugins():
    def __init__(self,list):
        self._maya_ver = list[0]
        self._plug_ver = list[1]
        self._license = list[2] if not list[2]=="" else ("client" if list[3] else "pro")
        self._driver = list[4] if len(list)==5 else ""
        self.BaseData()
        self.MakeClientDir()

    def BaseData(self):
        ## ---------------------------------------------------------------------------------
        ## change settings here
        self._plugin_name = 'redshift'
        self._b_dir = "B:"
        self._b_dist_path = "%s/plugins/maya" % self._b_dir
        self._plugin_software = "D:/plugins/maya/%s"%self._plugin_name
        ## ---------------------------------------------------------------------------------
        #获取 _plugin_software_path 路径 D:\PLUGINS\MAYA\REDSHIFT\software\driver0\redshift_2.5.32
        if self._driver == "": self._plugin_software_path = "%s/software/%s_%s"%(self._plugin_software,self._plugin_name,self._plug_ver.replace("",""))
        else: self._plugin_software_path = "%s/software/driver%s/%s_%s"%(self._plugin_software,self._driver,self._plugin_name,self._plug_ver.replace("",""))
        
        ## ---------------------------------------------------------------------------------
        ## change lic here or use the new lic from list[2]
        #获取 lic 码
        self._lic_code = "5059@127.0.0.1" if self._license=="pro" else list[2]

        self._GPU_Devices = '1080'

    def MakeClientDir(self):
        ## make all folders here 
        folders = ["source","software/temp","logs"]
        #添加 driver文件夹 及 temp文件夹
        if self._driver != '':
            folders.append("software/driver%s"%self._driver)
            folders.append("software/temp/driver%s/cache"%self._driver)
        else:
            folders.append("software/temp/cache")
        ## ---------------------------------------------------------------------------------
        #清掉之前的
        if os.path.exists("%s/%s"%(self._plugin_software,"software")):
            try:
                ## del the software folder in D/plugings
                subprocess.call("rd /s /q %s"%os.path.abspath("%s/%s"%(self._plugin_software,"software")),shell=True)
            except:
                self.PrintVr("Canot remove the software folder")
        #创建文件夹
        for elm in folders:
            if not os.path.exists("%s/%s"%(self._plugin_software,elm)):
                os.makedirs("%s/%s"%(self._plugin_software,elm))

    #检查B盘与本地文件 存在与否
    def SourceCheck(self,b_path,client_path):
        client_exist = [False,self._license]
        b_exist = [False,self._license]
        ## -------------------------------------------------------------------
        if self._license == "pro":
            pro_source = "%sformaya_%s.7z" % (self._plugin_name,self._plug_ver) ## goto D serch pro
            if not os.path.exists("%s/%s"%(client_path,pro_source)):                  ## goto B serch pro
                if not os.path.exists("%s/%s"%(b_path,pro_source)):
                    self.PrintVr("This version do not exist,install it Pl.")
                    plugM_software = pro_source
                else:
                    plugM_software = pro_source
                    b_exist = [True,self._license]
            else:
                plugM_software = pro_source
                client_exist = [True,self._license]
        return client_exist,b_exist,plugM_software
        
    def ConfigPlugin(self):
        ## ------------------------------------------
        ## copy source and unzip it in this founction
        ## ------------------------------------------
        self.PrintVr("ConfigPlugin proc")
        unztool = "C:/7-Zip"
        unzexe = "%s/7z.exe"%unztool
        if not os.path.exists(unzexe):
            b_unzip = "%s/tools/7-Zip"%self._b_dir
            os.system ("robocopy /e /ns /nc /nfl /ndl /np  %s %s" % (os.path.abspath(b_unzip), os.path.abspath(unztool)))
        plug_source = "%s/%s/source" % (self._b_dist_path,self._plugin_name)
        plug_aim = "%s/source" % self._plugin_software
        plug_software_info = self.SourceCheck(plug_source,plug_aim)
        self.PrintVr(plug_software_info)
        copy_source = True if (not plug_software_info[0][0] and plug_software_info[0][1]) else False
        ## ----------------------------------------------------------------------------------------------
        ## whether if it is the same file by getmtime
        ## if it is in D/plugins/***/source, but not the same with the file in B disk,then copy it again
        ## ----------------------------------------------------------------------------------------------
        if plug_software_info[0][0]:
            ## the source is in D/plugings
            if os.path.exists("%s/%s"%(plug_source,plug_software_info[2])):
                t1 = os.path.getmtime("%s/%s"%(plug_aim,plug_software_info[2]))
                t2 = os.path.getmtime("%s/%s"%(plug_source,plug_software_info[2]))
                if t1 !=t2:
                    copy_source = True
                    self.PrintVr("difference source, cp it...")
        if not plug_software_info[0][0] and not plug_software_info[1][0]:
            self.PrintVr("Cant found this version(All) ,to check the source for more informations. ")
            sys.exit(002)
        
        ## do the copy here, if erro,will try 3 times
        if copy_source:
            cp = 0
            while cp < 3:
                self.PrintVr("GET: %s"%plug_software_info[2])
                if os.path.exists("%s/%s"%(plug_source,plug_software_info[2])):
                    copy_log = open("%s/logs/copy_source.txt"%self._plugin_software,"wt")
                    cmds_copy = "copy %s %s" % (os.path.abspath("%s/%s"%(plug_source,plug_software_info[2])),
                                os.path.abspath("%s/%s"%(plug_aim,plug_software_info[2])))
                    #print(cmds_copy)
                    source_copy = subprocess.Popen(cmds_copy,stdout=copy_log,shell=True)
                    source_copy.wait()
                    cp =(cp+1) if not source_copy.returncode == 0 else 5
                    if source_copy.returncode == 0: copy_source = False
                    copy_log.close()
                else:
                    cp = 6
            if cp == 6:
                self.PrintVr('This plugin "%s" version %s is not exist.' % (self._plugin_name,self._plug_ver))
                sys.exit(55)
            elif cp == 3:
                self.PrintVr("Cant cp the source from the B disk.")
                sys.exit(555)
        ## ------------------------------------------------
        ## unzip the plugin file here,also will try 3 times
        ## ------------------------------------------------
        if not copy_source:
            self.PrintVr("Finally: %s/%s"%(plug_aim,plug_software_info[2]))
            unzip_times = 1
            while unzip_times<3:
                cmd_un7z_source = unzexe + " x -y -aos "
                cmd_un7z_source += "%s/%s"%(plug_aim,plug_software_info[2])
                cmd_un7z_source += " -o%s" % self._plugin_software_path
                # print(cmd_un7z_source)
                unzip_log = open("%s/logs/unzip.txt"%self._plugin_software,"wt")
                source_unzip = subprocess.Popen(cmd_un7z_source,stdout=unzip_log,shell=True)
                source_unzip.wait()
                if not source_unzip.returncode == 0:
                    ## re cp the source file
                    unzip_times +=1
                    os.system("copy %s %s /y" % (os.path.abspath("%s/%s"%(plug_source,plug_software_info[2])),
                                os.path.abspath("%s/%s"%(plug_aim,plug_software_info[2]))))
                else:
                    unzip_times = 3
                unzip_log.close()
    
    def RlmLicense(self):
        ## start the rlm server
        self.PrintVr("Try to del rlm_redshiftrlm")
        self.ServerToo(['rlm_redshift.exe'])
        #拷贝B盘的redshift_rlm_server_win64 到D盘
        srcDir1 = r"%s\%s\redshift_rlm_server_win64" % (self._b_dist_path,self._plugin_name)
        dstDir1 = r"D:\redshift_rlm_server_win64"
        if os.path.exists(dstDir1):
            try:
                subprocess.call("rd /s /q %s"%os.path.abspath(dstDir1),shell=True)
                self.PrintVr("del path %s" % dstDir1)
            except Exception, error:
                self.PrintVr("%s:%s"%(Exception,error) )
                self.PrintVr("Canot del path %s" % dstDir1)
        os.system("robocopy /e /ns /nc /nfl /ndl /np /NJS /NJH %s \"%s\"" % (srcDir1, dstDir1))

        #设置lic环境变量
        os.environ['REDSHIFT_LICENSE'] = self._lic_code
        os.environ['REDSHIFT_LICENSEPATH'] = r"D:/redshift_rlm_server_win64/redshift-core2.lic"
        self.PrintVr("REDSHIFT_LICENSEPATH is %s " % os.environ['REDSHIFT_LICENSEPATH'])
        #启动 rlm
        self.ServerToo([r'D:\redshift_rlm_server_win64\rlm_redshift.exe'],"start")


    def CreateEvn(self):
        ## make env informations here 
        # \\10.90.96.51\td1\plugins\maya\redshift\PREFS\1080\preferences.xml
        redshift_prefsPath = '%s/%s/%s%s' % ("%s/%s"%(self._b_dist_path,self._plugin_name), "PREFS", self._GPU_Devices, ".xml")
        #\\10.90.96.51\td1\plugins\maya\redshift
        redshift_d_path = self._plugin_software_path
        #旧的临时缓存路径 D:\PLUGINS\MAYA\REDSHIFT\software\temp\driver0\cache
        redshift_temp = "%s/software/%s" % (self._plugin_software,"temp/cache" if self._driver == "" else "temp/driver%s/cache"%self._driver)
        
        #创建新的临时缓存路径
        REDSHIFT_LOCALDATAPATH = r"D:/temp/REDSHIFT/CACHE"
        #gpuid为 显卡编号 1为第一张显卡 2位第二张显卡
        if os.environ.has_key('gpuid'):
            gid = int(os.environ.get('gpuid')) - 1            
            REDSHIFT_LOCALDATAPATH = 'D:/temp/REDSHIFT/CACHE/G%d' % gid
        if not os.path.exists(REDSHIFT_LOCALDATAPATH):
            os.makedirs(REDSHIFT_LOCALDATAPATH)      
        
        #设置环境变量
        os.environ['REDSHIFT_LOCALDATAPATH'] = REDSHIFT_LOCALDATAPATH
        os.environ['LOCALAPPDATA'] = REDSHIFT_LOCALDATAPATH
        
        ## get env values if its exist
        _REDSHIFT_MAYAEXTENSIONSPATH = os.environ.get('REDSHIFT_MAYAEXTENSIONSPATH')
        _MAYA_PLUG_IN_PATH = os.environ.get('MAYA_PLUG_IN_PATH')
        _MAYA_SCRIPT_PATH = os.environ.get('MAYA_SCRIPT_PATH')
        _MAYA_RENDER_DESC_PATH = os.environ.get('MAYA_RENDER_DESC_PATH')
        _PYTHONPATH = os.environ.get('PYTHONPATH')
        #redshift_d_path = D:\PLUGINS\MAYA\REDSHIFT\software\driver0\redshift_2.5.48
        #编写环境变量到env, 因为有些变量写入临时变量里面不起作用,所以写入maya.env
        path_line = "PATH=%PATH%;"+"%s/bin;"%redshift_d_path+r"C:/Program Files/Autodesk/Maya%s/bin"%self._maya_ver
        path_line +='\nREDSHIFT_COREDATAPATH = %s' % redshift_d_path
        path_line +='\nREDSHIFT_PLUG_IN_PATH = %s/Plugins/Maya/%s/nt-x86-64' % (redshift_d_path,self._maya_ver)
        path_line +='\nREDSHIFT_SCRIPT_PATH = %s/Plugins/Maya/Common/scripts' % redshift_d_path
        path_line +='\nREDSHIFT_XBMLANGPATH = %s/Plugins/Maya/Common/icons' % redshift_d_path
        path_line +='\nREDSHIFT_RENDER_DESC_PATH = %s/Plugins/Maya/Common/rendererDesc' % redshift_d_path
        path_line +='\nREDSHIFT_CUSTOM_TEMPLATE_PATH = %s/Plugins/Maya/Common/scripts/NETemplates' % redshift_d_path
        path_line +='\nREDSHIFT_MAYAEXTENSIONSPATH = %REDSHIFT_PLUG_IN_PATH%\extensions' + (";"+_REDSHIFT_MAYAEXTENSIONSPATH if _REDSHIFT_MAYAEXTENSIONSPATH else "")
        path_line +='\nREDSHIFT_PROCEDURALSPATH = %REDSHIFT_COREDATAPATH%\Procedurals'
        path_line +='\nMAYA_PLUG_IN_PATH = %s/Plugins/Maya/%s/nt-x86-64' % (redshift_d_path,self._maya_ver) + (";"+_MAYA_PLUG_IN_PATH if _MAYA_PLUG_IN_PATH else "")
        path_line +='\nMAYA_SCRIPT_PATH = %s/Plugins/Maya/Common/scripts' % redshift_d_path + (";"+_MAYA_SCRIPT_PATH if _MAYA_SCRIPT_PATH else "")
        path_line +='\nPYTHONPATH = %s/Plugins/Maya/Common/scripts' % redshift_d_path + (";"+_PYTHONPATH if _PYTHONPATH else "")
        path_line +='\nXBMLANGPATH = %s/Plugins/Maya/Common/icons' % redshift_d_path
        path_line +='\nMAYA_RENDER_DESC_PATH = %s/Plugins/Maya/Common/rendererDesc' % redshift_d_path + (";"+_MAYA_RENDER_DESC_PATH if _MAYA_RENDER_DESC_PATH else "")
        path_line +='\nMAYA_CUSTOM_TEMPLATE_PATH = %REDSHIFT_CUSTOM_TEMPLATE_PATH%'
        path_line +='\nREDSHIFT_PREFSPATH = ' + redshift_prefsPath
        path_line +='\nREDSHIFT_LOCALDATAPATH = %s' % REDSHIFT_LOCALDATAPATH
        path_line +='\nREDSHIFT_COMMON_ROOT = %s/Plugins/Maya/Common' % redshift_d_path
        path_line +='\nLOCALAPPDATA = %s' % REDSHIFT_LOCALDATAPATH
        return path_line
 
    def MappingEVN(self):
        ## ----------------------------------------------------
        ## check maya version in the plugings folder of redshift
        #self._plugin_software_path = D:\PLUGINS\MAYA\REDSHIFT\software\driver0\redshift_2.5.48
        if os.path.exists(self._plugin_software_path):
            maya_ver_check_path = "%s/Plugins/Maya/%s" % (self._plugin_software_path,self._maya_ver)
            if not os.path.exists(maya_ver_check_path):
                self.PrintVr("This RS version do not for maya %s"%self._maya_ver)
                sys.exit(004)
        #我的文档maya路径
        env_path = r"C:\Users\enfuzion\Documents\maya\%s\Maya.env"%(self._maya_ver if float(self._maya_ver)>2015 else "%s-x64"%self._maya_ver)
        ## create maya.env file
        if not os.path.exists(os.path.dirname(env_path)): os.makedirs(os.path.dirname(env_path))
        with open(env_path,"w") as f:
            f.write(self.CreateEvn().replace("/","\\"))
            f.close()
        ## copy redshiftRenderer.xml file
        #拷贝 xml 到本地C盘
        dstDir1 = "%s/Plugins/Maya/Common/rendererDesc/redshiftRenderer.xml"%(self._plugin_software_path)
        dstDir2 = r"C:\Program Files\Autodesk\Maya%s\bin\rendererDesc\redshiftRenderer.xml"%self._maya_ver
        cmds = 'copy /y %s "%s"'%(os.path.abspath(dstDir1),os.path.abspath(dstDir2))
        # print cmds
        subprocess.call(cmds,shell=True)

    def PrintVr(self,info,extr="RedshiftSetup"):
        if str(info).strip() != "":
            print("[%s] %s"%(extr,str(info)))

    @staticmethod
    def ServerToo(apps=[],method='kill',platform='win'):
        if method == "kill":
            for app in apps:
                if not platform=='Linux':
                    cmds = r'c:\windows\system32\cmd.exe /c c:\windows\system32\TASKKILL.exe /F /IM %s'%app
                elif platform=='Linux':
                    cmds = ''
                subprocess.call(cmds,shell=True)
        elif method == "start":
            for app in apps:
                if not platform=='Linux':
                    cmds = r'start %s'%app
                elif platform=='Linux':
                    cmds = ''
                subprocess.call(cmds,shell=True)

def main(maya_ver="2016",plug_ver="3.60.04"):
    ## ------------------------------------------------------------
    ## eg. [maya_version,vray_version,license_type,use_new_license,driver]
    ## create by shen 2018.03.301705
    ## ------------------------------------------------------------
    use_new_license = False
    new_license = ''
    #判断是否双显,获取基本路径信息及创建基本文件夹
    if os.environ.has_key('gpuid'):
        gpu_card = int(os.environ.get('gpuid')) - 1
        plug_ins = PlugPlugins([maya_ver,plug_ver,new_license,use_new_license,str(gpu_card)])
    else:
        plug_ins = PlugPlugins([maya_ver,plug_ver,new_license,use_new_license])
    #拷贝z7 并解压
    plug_ins.ConfigPlugin()
    #设置环境变量写入到maya.env ,拷贝xml到本地C盘
    plug_ins.MappingEVN()
    #拷贝rlm文件夹到本地D盘,设置环境变量,启动rlm
    plug_ins.RlmLicense()
    plug_ins.PrintVr("Pluging setup finished.")
    return plug_ins

def doConfigSetup(*args):
    clientInfo = args[0]
    maya_ver = clientInfo.swVer()
    all_plgins = clientInfo.plgins()
    rs_ver = all_plgins["redshift_GPU"] if "redshift_GPU" in all_plgins else False
    if not rs_ver:
        print("PL set an redshift version")
        sys.exit(003)
    main(maya_ver,rs_ver)

if __name__=="__main__":
    
    os.system(r'"C:\Program Files\Autodesk\Maya%s\bin\maya.exe"'%main('2016','2.0.47')._maya_ver)
    
