#!/usr/bin/python

from merge_utils import *
import glob
import re
import portage

progPath =  sys.argv[0].split("/")
if(len(progPath) > 1):
  pwd = "/".join(progPath[0:-1])
  print pwd
  cwd = pwd
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
cb_pkgs = os.popen(cwd +"/cb-get-pkgs.sh "+ cb_overlay.root.rstrip("/"),"r").readlines()
funtoo_pkgs = []
weevil_pkgs = []
for x in fun_pkgs: 
  funtoo_pkgs.append(x.lstrip().rstrip())
for x in cb_pkgs:
  weevil_pkgs.append(x.lstrip().rstrip())


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

ebDel = []
for weevil_pkg in weevil_pkgs:
  try:
    funtoo_pkgs.index(weevil_pkg)
  except:
    try:
      eBuildList.index(weevil_pkg)
    except:
      ebDel.append(weevil_pkg)
print("FOR DELETE : "+ str(ebDel))

steps = [
  GitPull(branch),
  SyncTree(cb_overlay),
  SyncDir(funtoo_overlay.root,"licenses"),
  SyncDir(funtoo_overlay.root,"eclass"),
  SyncDir(funtoo_overlay.root,"metadata"),
  SyncDir(funtoo_overlay.root,"profiles","profiles", exclude=["repo_name","categories","package.mask","package.unmask","package.use"]),
  SyncDir(funtoo_overlay.root,"funtoo","funtoo", exclude=["scripts"])
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
  
  for eb in ebDel:
    try:
      os.system("rm -frv "+ work.root.rstrip("/") +"/"+ eb +"/")
    except:
      print("Error in deleting ebuild : "+ work.root.rstrip("/") +"/"+ eb +"/")
    
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
    os.system("rsync -av --delete-after "+ funtoo_mask +" "+ work.root.rstrip("/") +"/profiles/package.mask/")
    if(len(cb_masks) > 0):
      for cb_mask in cb_masks:
	pkgName = cb_mask[0] +"/"+ cb_mask[1]
	os.system("sed -i \'/"+ cb_mask[0] +"\\/"+ cb_mask[1] +"/d\' "+ work.root.rstrip("/") +"/profiles/package.mask/" + funtoo_mask.split("/")[-1])
      
      

  cb_unmasks_Full = open(cb_overlay.root.rstrip("/") + "/profiles/package.unmask/cb","r").readlines()
  cb_unmasks = []
  for cbum in cb_unmasks_Full:
    if(re.match(r'^\s*$', cbum)):
      continue
    if(cbum.find("#") == 0):
      continue
    cb_unmasks.append(portage.catpkgsplit(cbum.lstrip(">").lstrip("<").lstrip("=").lstrip(">").lstrip("<").lstrip("=").rstrip()))
  funtoo_unmasks = glob.glob(funtoo_overlay.root.rstrip("/") + "/profiles/package.unmask/*")
  for funtoo_unmask in funtoo_unmasks:
    os.system("rsync -av --delete-after "+ funtoo_unmask +" "+ work.root.rstrip("/") +"/profiles/package.unmask/")
    if(len(cb_unmasks) > 0):
      for cb_unmask in cb_unmasks:
	pkgName = cb_unmask[0] +"/"+ cb_unmask[1]
	os.system("sed -i \'/"+ cb_unmask[0] +"\\/"+ cb_unmask[1] +"/d\' "+ work.root.rstrip("/") +"/profiles/package.unmask/" + funtoo_unmask.split("/")[-1])
      
      
      
  cb_use_Full = open(cb_overlay.root.rstrip("/") + "/profiles/package.use/cb","r").readlines()
  cb_uses = []
  for cbu in cb_use_Full:
    if(re.match(r'^\s*$', cbu)):
      continue
    if(cbu.find("#") == 0):
      continue
    cbuu = cbu.split()
    cb_uses.append(cbuu[0].lstrip(">").lstrip("<").lstrip("=").lstrip(">").lstrip("<").lstrip("=").rstrip())
  funtoo_uses = glob.glob(funtoo_overlay.root.rstrip("/") + "/profiles/package.use/*")
  for funtoo_use in funtoo_uses:
    os.system("rsync -av --delete-after "+ funtoo_use +" "+ work.root.rstrip("/") +"/profiles/package.use/")
    if(len(cb_uses) > 0):
      for cb_use in cb_uses:
	pkgName = cb_use[0] +"/"+ cb_use[1]
	os.system("sed -i \'/"+ cb_use[0] +"\\/"+ cb_use[1] +"/d\' "+ work.root.rstrip("/") +"/profiles/package.use/" + funtoo_use.split("/")[-1])
      



  work.gitCommit(message="sync upstream funtoo-overlay updates",push=push)
  




  
