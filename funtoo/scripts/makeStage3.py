#!/usr/bin/python

import os

catalyst = "/usr/bin/catalyst"

if(not os.path.exists("/var/tmp/catalyst/lastuuid")):
  os.system("/usr/bin/uuidgen > /var/tmp/catalyst/lastuuid")
else:
  


test = os.system(catalyst)
print(":"+ str(test) +":")
