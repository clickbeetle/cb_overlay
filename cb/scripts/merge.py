#!/usr/bin/python2

from merge_utils import *

gentoo_src = Tree("gentoo","gentoo.org", "git://github.com/clickbeetle/cb_gentoo.git", pull=True, trylocal="/BACKUP/clickbeetleCook.DO_NO_DELETE/git/cb_gentoo")
cb_overlay = Tree("cb-overlay", branch, "git://github.com/clickbeetle/cb_overlay.git", pull=True)
foo_overlay = Tree("foo-overlay", "master", "https://github.com/slashbeast/foo-overlay.git", pull=True)
bar_overlay = Tree("bar-overlay", "master", "git://github.com/adessemond/bar-overlay.git", pull=True)
#flora_overlay = Tree("flora", "master", "git://github.com/funtoo/flora.git", pull=True)

steps = [
  SyncTree(gentoo_src,exclude=["/metadata/cache/**","ChangeLog", "dev-util/metro"]),
  #ApplyPatchSeries("%s/funtoo/patches" % cb_overlay.root ),
  
  # masking this untill i get a good bandwidth to host distfiles
  #ThirdPartyMirrors(),
  
  InsertEbuilds(foo_overlay, select="all", skip=None, replace=["app-shells/rssh","net-misc/unison"]),
  InsertEbuilds(bar_overlay, select="all", skip=None, replace=True),
#  InsertEbuilds(flora_overlay, select="all", skip=None, replace=False)
]

# Progress overlay merge
if not os.path.exists("/usr/bin/svn"):
    print("svn binary not found at /usr/bin/svn. Exiting.")
    sys.exit(1)
#progress_overlay = SvnTree("progress", "https://gentoo-progress.googlecode.com/svn/overlays/progress")
steps.extend((
    #SyncFiles(progress_overlay.root, {
        #"profiles/package.mask":"profiles/package.mask/progress",
        #"profiles/use.mask":"profiles/use.mask/progress"
    #}),
    SyncDir(cb_overlay.root,"profiles","profiles", exclude=["repo_name","categories"]),
    ProfileDepFix(),
    SyncDir(cb_overlay.root,"licenses"),
#    SyncDir(progress_overlay.root, "eclass"),
    
    SyncDir(cb_overlay.root,"eclass"),
    SyncDir(cb_overlay.root,"metadata"),
    InsertEbuilds(cb_overlay, select="all", skip=None, replace=True),
    #InsertEbuilds(progress_overlay, select="all", skip=None, replace=True, merge=["dev-lang/python", "dev-libs/boost", "dev-python/psycopg", "dev-python/pysqlite", "dev-python/python-docs", "dev-python/simpletal", "dev-python/wxpython", "x11-libs/vte"])
 #   InsertEbuilds(progress_overlay, select="all", skip=None, replace=True)
))

steps.extend((
  Minify(),
  GenCache()
))

# work tree is a non-git tree in tmpfs for enhanced performance - we do all the heavy lifting there:

work = UnifiedTree("/tmp/merge-%s" % os.path.basename(dest[0]),steps)
work.run()


cb_masks_Full = open(cb_overlay.root.rstrip("/") + "/profiles/package.mask/cb","r").readlines()
cb_masks = []
for cbm in cb_masks_Full:
  if(re.match(r'^\s*$', cbm)):
    continue
  if(cbm.find("#") == 0):
    continue
  cb_masks.append(portage.catpkgsplit(cbm.lstrip(">").lstrip("<").lstrip("=").lstrip(">").lstrip("<").lstrip("=").rstrip()))
gentoo_masks = glob.glob(gentoo_src.root.rstrip("/") + "/profiles/package.mask/*")
for gentoo_mask in gentoo_masks:
  os.system("rsync -av --delete-after "+ gentoo_mask +" "+ work.root.rstrip("/") +"/profiles/package.mask/")
  if(len(cb_masks) > 0):
    print cb_masks
    for cb_mask in cb_masks:
      if(cb_mask):
        pkgName = cb_mask[0] +"/"+ cb_mask[1]
        os.system("sed -i \'/"+ cb_mask[0] +"\\/"+ cb_mask[1] +"/d\' "+ work.root.rstrip("/") +"/profiles/package.mask/" + gentoo_mask.split("/")[-1])
#progress_masks = glob.glob(progress_overlay.root.rstrip("/") + "/profiles/package.mask/*")
#for progress_mask in progress_masks:
  #os.system("rsync -av --delete-after "+ progress_mask +" "+ work.root.rstrip("/") +"/profiles/package.mask/")
  #if(len(cb_masks) > 0):
    #print cb_masks
    #for cb_mask in cb_masks:
      #if(cb_mask):
        #pkgName = cb_mask[0] +"/"+ cb_mask[1]
        #os.system("sed -i \'/"+ cb_mask[0] +"\\/"+ cb_mask[1] +"/d\' "+ work.root.rstrip("/") +"/profiles/package.mask/" + progress_mask.split("/")[-1])
    

cb_unmasks_Full = open(cb_overlay.root.rstrip("/") + "/profiles/package.unmask/cb","r").readlines()
cb_unmasks = []
for cbum in cb_unmasks_Full:
  if(re.match(r'^\s*$', cbum)):
    continue
  if(cbum.find("#") == 0):
    continue
  cb_unmasks.append(portage.catpkgsplit(cbum.lstrip(">").lstrip("<").lstrip("=").lstrip(">").lstrip("<").lstrip("=").rstrip()))
gentoo_unmasks = glob.glob(gentoo_src.root.rstrip("/") + "/profiles/package.unmask/*")
for gentoo_unmask in gentoo_unmasks:
  os.system("rsync -av --delete-after "+ gentoo_unmask +" "+ work.root.rstrip("/") +"/profiles/package.unmask/")
  if(len(cb_unmasks) > 0):
    for cb_unmask in cb_unmasks:
      if(cb_unmask):
        pkgName = cb_unmask[0] +"/"+ cb_unmask[1]
        os.system("sed -i \'/"+ cb_unmask[0] +"\\/"+ cb_unmask[1] +"/d\' "+ work.root.rstrip("/") +"/profiles/package.unmask/" + gentoo_unmask.split("/")[-1])
#progress_unmasks = glob.glob(progress_overlay.root.rstrip("/") + "/profiles/package.unmask/*")
#for progress_unmask in progress_unmasks:
  #os.system("rsync -av --delete-after "+ progress_unmask +" "+ work.root.rstrip("/") +"/profiles/package.unmask/")
  #if(len(cb_unmasks) > 0):
    #for cb_unmask in cb_unmasks:
      #if(cb_unmask):
        #pkgName = cb_unmask[0] +"/"+ cb_unmask[1]
        #os.system("sed -i \'/"+ cb_unmask[0] +"\\/"+ cb_unmask[1] +"/d\' "+ work.root.rstrip("/") +"/profiles/package.unmask/" + progress_unmask.split("/")[-1])
        
    
    
cb_use_Full = open(cb_overlay.root.rstrip("/") + "/profiles/package.use/cb","r").readlines()
cb_uses = []
for cbu in cb_use_Full:
  if(re.match(r'^\s*$', cbu)):
    continue
  if(cbu.find("#") == 0):
    continue
  cbuu = cbu.split()
  cb_uses.append(cbuu[0].lstrip(">").lstrip("<").lstrip("=").lstrip(">").lstrip("<").lstrip("=").rstrip())
gentoo_uses = glob.glob(gentoo_src.root.rstrip("/") + "/profiles/package.use/*")
for gentoo_use in gentoo_uses:
  os.system("rsync -av --delete-after "+ gentoo_use +" "+ work.root.rstrip("/") +"/profiles/package.use/")
  if(len(cb_uses) > 0):
    for cb_use in cb_uses:
      if(cb_use):
        pkgName = cb_use[0] +"/"+ cb_use[1]
        os.system("sed -i \'/"+ cb_use[0] +"\\/"+ cb_use[1] +"/d\' "+ work.root.rstrip("/") +"/profiles/package.use/" + gentoo_use.split("/")[-1])
#progress_uses = glob.glob(progress_overlay.root.rstrip("/") + "/profiles/package.use/*")
#for progress_use in progress_uses:
  #os.system("rsync -av --delete-after "+ progress_use +" "+ work.root.rstrip("/") +"/profiles/package.use/")
  #if(len(cb_uses) > 0):
    #for cb_use in cb_uses:
      #if(cb_use):
        #pkgName = cb_use[0] +"/"+ cb_use[1]
        #os.system("sed -i \'/"+ cb_use[0] +"\\/"+ cb_use[1] +"/d\' "+ work.root.rstrip("/") +"/profiles/package.use/" + progress_use.split("/")[-1])


cb_use_desc = cb_overlay.root.rstrip("/") + "/profiles/use.desc"
gentoo_use_desc = gentoo_src.root.rstrip("/") + "/profiles/use.desc"
#progress_use_desc = progress_overlay.root.rstrip("/") + "/profiles/use.desc"
work_use_desc = work.root.rstrip("/") +"/profiles/use.desc"
os.system("cat "+ cb_use_desc +" | grep -iv ^# > "+ work_use_desc)
os.system("cat "+ gentoo_use_desc +" | grep -iv ^# >> "+ work_use_desc)
#os.system("cat "+ progress_use_desc +" | grep -iv ^# >> "+ work_use_desc)
os.system("sort "+ work_use_desc +" -o "+ work_use_desc)

os.system("grep DELETE "+ cb_use_desc +" | gawk '{print $2}' > /tmp/cb_use_desc.pat")
os.system("sed -i '/^$/d' /tmp/cb_use_desc.pat")
os.system("grep -v --file=/tmp/cb_use_desc.pat "+ work_use_desc +" > "+ work_use_desc +".revved")
os.system("rm -fv "+ work_use_desc)
os.system("mv "+ work_use_desc +".revved "+ work_use_desc)



cb_local_use_desc = cb_overlay.root.rstrip("/") + "/profiles/use.local.desc"
gentoo_local_use_desc = gentoo_src.root.rstrip("/") + "/profiles/use.local.desc"
#progress_local_use_desc = progress_overlay.root.rstrip("/") + "/profiles/use.local.desc"
work_local_use_desc = work.root.rstrip("/") +"/profiles/use.local.desc"
os.system("cat "+ cb_local_use_desc +" | grep -iv ^# > "+ work_local_use_desc)
os.system("cat "+ gentoo_local_use_desc +" | grep -iv ^# >> "+ work_local_use_desc)
#os.system("cat "+ progress_local_use_desc +" | grep -iv ^# >> "+ work_local_use_desc)
os.system("sort "+ work_local_use_desc +" -o "+ work_local_use_desc)

os.system("grep DELETE "+ cb_local_use_desc +" | gawk '{print $2}' > /tmp/cb_local_use_desc.pat")
os.system("sed -i '/^$/d' /tmp/cb_local_use_desc.pat")
os.system("grep -v --file=/tmp/cb_local_use_desc.pat "+ work_local_use_desc +" > "+ work_local_use_desc +".revved")
os.system("rm -fv "+ work_local_use_desc)
os.system("mv "+ work_local_use_desc +".revved "+ work_local_use_desc)

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
    runShell("( cd %s; git checkout -b master; git rm -f README; git commit -a -m 'initial clickbeetle.in commit' )" % ( d ) )
    print("Pushing disabled automatically because repository created from scratch.")
    push = False
  prod = UnifiedTree(d,steps)
  prod.run()
  
          
          
  prod.gitCommit(message="glorious clickbeetle updates",push=push)
