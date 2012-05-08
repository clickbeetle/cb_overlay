#!/usr/bin/python

from merge_utils import *
import glob
import re
import portage

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
  if(re.match(r'^\s*$',ebl)):
    continue
  if(ebl.find("#") == 0):
    continue
  eBuildList.append(ebl.rstrip().lstrip())
  
cb_overlay = Tree("cb-overlay","master", "git://github.com/clickbeetle/cb_overlay.git", pull=True)
funtoo_overlay = Tree("funtoo-overlay", "master", "git://github.com/funtoo/funtoo-overlay.git", pull=True)





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
    print("WTF error : "+ ebl)
    continue



steps = [
  GitPull(branch),
  SyncTree(cb_overlay),
  SyncDir(funtoo_overlay.root,"licenses"),
  SyncDir(funtoo_overlay.root,"eclass"),
  SyncDir(funtoo_overlay.root,"metadata"),
  SyncDir(funtoo_overlay.root,"profiles","profiles", exclude=["repo_name","categories","package.mask","package.unmask","package.use"]),
  SyncDir(funtoo_overlay.root,"virtual")
]


for des in dest:
  d = des.rstrip("/")
  work = UnifiedTree(d,steps)
  work.run()

  for eb in ebSend:
    if(not os.path.exists(work.root.rstrip("/") +"/"+ eb +"/")):
      try:
        os.makedirs(work.root.rstrip("/") +"/"+ eb +"/")
      except:
        print("Error in making ebuild : "+ work.root.rstrip("/") +"/"+ eb +"/")
        os.exit(1)
    os.system("rsync -av --delete-after "+ funtoo_overlay.root.rstrip("/") +"/"+ eb +"/ "+ work.root.rstrip("/") +"/"+ eb +"/")
    
  cb_masks_Full = open(cb_overlay.root.rstrip("/") + "/profiles/package.mask/cb","r").readlines()
  cb_masks = []
  for cbm in cb_masks_Full:
    if(re.match(r'^\s*$', cbm)):
      continue
    if(cbm.find("#") == 0):
      continue
    
    cb_masks.append(portage.catpkgsplit(cbm.lstrip(">").lstrip("<").lstrip("=").lstrip(">").lstrip("<").lstrip("=").rstrip()))
  
  funtoo_masks = glob.glob(funtoo_overlay.root.rstrip("/") + "/profiles/package.mask/*")
  for funtoo_mask in funtoo_masks:
    for cb_mask in cb_masks:
      pkgName = cb_mask[0] +"/"+ cb_mask[1]
      os.system("sed \'/"+ cb_mask[0] +"\\/"+ cb_mask[1] +"/d\' "+ funtoo_mask +" > "+ work.root.rstrip("/") +"/profiles/package.mask/" + funtoo_mask.split("/")[-1])

  work.gitCommit(message="sync upstream funtoo-overlay updates",push=push)
  




  
