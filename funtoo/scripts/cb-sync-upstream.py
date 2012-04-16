#!/usr/bin/python

from merge_utils import *

progPath =  sys.argv[0].split("/")
cwd = os.getcwd()
if(len(progPath) > 1):
  pwd = "/".join(progPath[0:-1])
  print pwd
  cwd = cwd.rstrip("/") +"/"+ pwd
else:
  cwd = os.getcwd()
  
eBuildList = []
ebFile = open(cwd +"/cb-sync-upstream.exclude","r")
for ebl in ebFile.readlines():
  if(ebl.find("#") == 0):
    continue
  eBuildList.append(ebl.rstrip().lstrip())
  
cb_overlay = Tree("cb-overlay","master", "git://github.com/clickbeetle/cb_overlay.git", pull=True)
funtoo_overlay = Tree("funtoo-overlay", "master", "git://github.com/funtoo/funtoo-overlay.git", pull=True)

fun_pkgs = os.popen(cwd +"/cb-get-pkgs.sh "+ funtoo_overlay.root.rstrip("/"),"r").readlines()
funtoo_pkgs = []
for x in fun_pkgs: 
  funtoo_pkgs.append(x.lstrip().rstrip())
for f_pkgs in funtoo_pkgs:
  if(sys.path.exists(cb_overlay.root.rstrp("/") + f_pkgs):
    print(f_pkgs + " exists"

#for ebl in eBuildList:
  #if(ebl):
    #os.system("mkdir -p "+ cb_ports_locked.root.rstrip("/") + "/" + ebl.rstrip("/").lstrip("/"))
    #os.system("rsync -av "+ cb_ports.root.rstrip("/") + "/" + ebl.rstrip("/").lstrip("/") + "/ "+  cb_ports_locked.root.rstrip("/") + "/" + ebl.rstrip("/").lstrip("/") + "/")
