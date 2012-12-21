#!/bin/bash
if [ ! $1 ]; then
  echo "please provide a branch name to update to the latest cb_ports"
  exit 1
fi

echo "updating branch $1"
cd /BACKUP/clickbeetleCook.DO_NO_DELETE/git/cb_ports_locked/
git pull
if [ $? != 0 ]; then 
  echo "error on branch $1"
  exit 1
fi

git checkout $1
if [ $? != 0 ]; then 
  echo "error on branch $1"
  exit 1
fi


cd /BACKUP/clickbeetleCook.DO_NO_DELETE/git/cb_ports/
git pull
if [ $? != 0 ]; then 
  echo "error on branch $1"
  exit 1
fi
cd /BACKUP/clickbeetleCook.DO_NO_DELETE/git/cb_ports_locked/
rsync -av /BACKUP/clickbeetleCook.DO_NO_DELETE/git/cb_ports/ /BACKUP/clickbeetleCook.DO_NO_DELETE/git/cb_ports_locked/ --exclude=.git --delete
git add .
git commit -a -m "updates for $1 branch :)"
git push -u origin $1




 