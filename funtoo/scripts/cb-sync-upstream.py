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

steps = [
  SyncTree(cb_overlay),
  SyncDir(funtoo_overlay.root,"licenses"),
  SyncDir(funtoo_overlay.root,"eclass"),
  SyncDir(funtoo_overlay.root,"metadata"),
  SyncDir(funtoo_overlay.root,"profiles","profiles", exclude=["repo_name","categories"]),
  SyncDir(funtoo_overlay.root,"virtual"),
  ProfileDepFix()
]

work = UnifiedTree("/dev/shm/merge-%s" % os.path.basename(dest[0]),steps)
work.run()





fun_pkgs = os.popen(cwd +"/cb-get-pkgs.sh "+ funtoo_overlay.root.rstrip("/"),"r").readlines()
funtoo_pkgs = []
for x in fun_pkgs: 
  funtoo_pkgs.append(x.lstrip().rstrip())



pkgs_alive = []
pkgs_dead = []

for f_pkgs in funtoo_pkgs:
  if(os.path.exists(cb_overlay.root.rstrip("/") +"/"+ f_pkgs)):
    pkgs_alive.append(cb_overlay.root.rstrip("/") +"/"+ f_pkgs)
  else:
    pkgs_dead.append(cb_overlay.root.rstrip("/") +"/"+ f_pkgs)

ebSend = funtoo_pkgs
for ebl in eBuildList:
  try:
    ebSend.index(ebl)
    ebSend.remove(ebl)
    print("Not syncing pkg : "+ ebl)
  except:
    print("WTF error")
    continue
  
for eb in ebSend:
  print("rsync -av --delete-after "+ funtoo_overlay.root.rstrip("/") +"/"+ eb +"/ "+ work.root.rstrip("/") +"/"+ eb +"/")

  
#steps = [
  #GitPrep(branch),
  #SyncTree(work),
#]
  

  
  
  
  
  
  
#for d in dest:
  #if not os.path.isdir(d):
    #os.makedirs(d)
  #if not os.path.isdir("%s/.git" % d):
    #runShell("( cd %s; git init )" % d )
    #runShell("echo 'created by merge.py' > %s/README" % d )
    #runShell("( cd %s; git add README; git commit -a -m 'initial commit by merge.py' )" % d )
    #runShell("( cd %s; git checkout -b "+ branch +"; git rm -f README; git commit -a -m 'initial clickbeetle.in commit' )" % ( d ) )
    #print("Pushing disabled automatically because repository created from scratch.")
    #push = False
  #prod = UnifiedTree(d,steps)
  #prod.run()
  #prod.gitCommit(message="sync upstream funtoo-overlay updates",push=push)
