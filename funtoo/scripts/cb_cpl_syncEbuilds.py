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
  eBuildList.append(ebl.rstrip().lstrip())

print cwd +"/cb_cpl."+ branch
print dest





cb_ports = Tree("gentoo","master", "git://github.com/clickbeetle/cb_ports.git", pull=True, trylocal="/BACKUP/clickbeetleCook.DO_NO_DELETE/git/cb_ports")

for ebl in eBuildList:
  print cb_ports.root + "/" + ebl 
  
  
  
  

#steps = [
  #Minify(),
  #GenCache()
#]

## work tree is a non-git tree in tmpfs for enhanced performance - we do all the heavy lifting there:

#work = UnifiedTree("/BACKUP/clickbeetleCook.DO_NO_DELETE/src/merge-%s" % os.path.basename(dest[0]),steps)
#work.run()

#steps = [
  #GitPrep(branch),
  #SyncTree(work)
#]

## then for the production tree, we rsync all changes on top of our prod git tree and commit:

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
  #prod.gitCommit(message="glorious clickbeetle updates",push=push)













