#!/usr/bin/python


from merge_utils import *


print branch
progPath =  sys.argv[0].split("/")
cwd = os.getcwd()
if(len(progPath) > 1):
  pwd = "/".join(progPath[0:-1])
  print pwd
  cwd = cwd.rstrip("/") +"/"+ pwd
else:
  cwd = os.getcwd()
  
eBuildList = []
ebFile = open(cwd +"/cb_cpl."+ branch,"r")
for ebl in ebFile.readlines():
<<<<<<< HEAD
  if ( ebl.find("#") == 0):
=======
  if(ebl.find("#") == 0):
>>>>>>> 7977b1cdf68c1b6d19491e34b19c31de2fd92d1f
    continue
  eBuildList.append(ebl.rstrip().lstrip())

print cwd +"/cb_cpl."+ branch
print dest[0]





cb_ports = Tree("gentoo","master", "git://github.com/clickbeetle/cb_ports.git", pull=True, trylocal="/BACKUP/clickbeetleCook.DO_NO_DELETE/git/cb_ports")
<<<<<<< HEAD
#cb_ports_locked = Tree("cpl",branch,"git@github.com:clickbeetle/cb_ports_locked.git", pull=True, trylocal="/BACKUP/clickbeetleCook.DO_NO_DELETE/git/cb_ports_locked")

  


for ebl in eBuildList:
  print("mkdir -p "+ dest[0].rstrip("/") + "/" + ebl.rstrip("/").lstrip("/"))
  print("rsync -av "+ cb_ports.root + "/" + ebl.rstrip("/").lstrip("/") + "/ "+ dest[0].rstrip("/") + "/" + ebl.rstrip("/").lstrip("/") + "/")
  
  
  
  
  
  

steps = [
=======
cb_ports_locked = Tree("cbl",branch, "git@github.com:clickbeetle/cb_ports_locked.git", pull=True)


for ebl in eBuildList:
  if(ebl):
    os.system("mkdir -p "+ cb_ports_locked.root.rstrip("/") + "/" + ebl.rstrip("/").lstrip("/"))
    os.system("rsync -av "+ cb_ports.root.rstrip("/") + "/" + ebl.rstrip("/").lstrip("/") + "/ "+  cb_ports_locked.root.rstrip("/") + "/" + ebl.rstrip("/").lstrip("/") + "/")
  

steps = [
  SyncTree(cb_ports_locked),
  ProfileDepFix(),
  SyncDir(cb_ports.root,"licenses"),
  SyncDir(cb_ports.root,"eclass"),
  SyncDir(cb_ports.root,"metadata"),
>>>>>>> 7977b1cdf68c1b6d19491e34b19c31de2fd92d1f
  Minify(),
  GenCache()
]

## work tree is a non-git tree in tmpfs for enhanced performance - we do all the heavy lifting there:

work = UnifiedTree("/dev/shm/merge-%s" % os.path.basename(dest[0]),steps)
work.run()

steps = [
  GitPrep(branch),
  SyncTree(work)
]

# then for the production tree, we rsync all changes on top of our prod git tree and commit:

for d in dest:
  if not os.path.isdir(d):
    os.makedirs(d)
  if not os.path.isdir("%s/.git" % d):
    runShell("( cd %s; git init )" % d )
    runShell("echo 'created by merge.py' > %s/README" % d )
    runShell("( cd %s; git add README; git commit -a -m 'initial commit by merge.py' )" % d )
    runShell("( cd %s; git checkout -b "+ branch +"; git rm -f README; git commit -a -m 'initial clickbeetle.in commit' )" % ( d ) )
    print("Pushing disabled automatically because repository created from scratch.")
    push = False
  prod = UnifiedTree(d,steps)
  prod.run()
  prod.gitCommit(message="sync ebuild updates",push=push)














