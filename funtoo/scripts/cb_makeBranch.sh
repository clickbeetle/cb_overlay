#!/bin/bash
rsync -av /home/shrinidhi/bin/gitHub/cb_ports/ /home/shrinidhi/bin/gitHub/cb_ports_locked/ --exclude=.git
cd /home/shrinidhi/bin/gitHub/cb_ports_locked/
git add .
git commit -a -m "updates for studio branch :)"
git push -u origin studio




 
