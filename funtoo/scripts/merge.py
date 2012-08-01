#!/usr/bin/python2

from merge_utils import *

gentoo_src = Tree("gentoo","gentoo.org", "git://github.com/clickbeetle/cb_gentoo.git", pull=True, trylocal="/BACKUP/clickbeetleCook.DO_NO_DELETE/git/cb_gentoo")
cb_overlay = Tree("cb-overlay", branch, "git://github.com/clickbeetle/cb_overlay.git", pull=True)
foo_overlay = Tree("foo-overlay", "master", "https://github.com/slashbeast/foo-overlay.git", pull=True)
bar_overlay = Tree("bar-overlay", "master", "git://github.com/adessemond/bar-overlay.git", pull=True)
flora_overlay = Tree("flora", "master", "git://github.com/funtoo/flora.git", pull=True)

steps = [
  SyncTree(gentoo_src,exclude=["/metadata/cache/**","ChangeLog", "dev-util/metro"]),
  #ApplyPatchSeries("%s/funtoo/patches" % cb_overlay.root ),
  
  # masking this untill i get a good bandwidth to host distfiles
  #ThirdPartyMirrors(),
  SyncDir(cb_overlay.root,"profiles","profiles", exclude=["repo_name","categories"]),
  ProfileDepFix(),
  #SyncDir(cb_overlay.root,"licenses"),
  SyncDir(cb_overlay.root,"eclass"),
  SyncDir(cb_overlay.root,"metadata"),
  InsertEbuilds(cb_overlay, select="all", skip=None, replace=True),
  InsertEbuilds(foo_overlay, select="all", skip=None, replace=["app-shells/rssh","net-misc/unison"]),
  InsertEbuilds(bar_overlay, select="all", skip=None, replace=True),
  InsertEbuilds(flora_overlay, select="all", skip=None, replace=False)
]

# Progress overlay merge
if not os.path.exists("/usr/bin/svn"):
    print("svn binary not found at /usr/bin/svn. Exiting.")
    sys.exit(1)
progress_overlay = SvnTree("progress", "https://gentoo-progress.googlecode.com/svn/overlays/progress")
steps.extend((
    SyncDir(progress_overlay.root, "eclass"),
    SyncFiles(progress_overlay.root, {
        "profiles/package.mask":"profiles/package.mask/progress",
        "profiles/use.mask":"profiles/use.mask/progress"
    }),
    InsertEbuilds(progress_overlay, select="all", skip=None, replace=True, merge=["dev-lang/python", "dev-libs/boost", "dev-python/psycopg", "dev-python/pysqlite", "dev-python/python-docs", "dev-python/simpletal", "dev-python/wxpython", "x11-libs/vte"])
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
