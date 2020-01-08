# !/usr/bin/env python              # Let's build another tool together
import f5_admin                     # First we need to let Python know we're going to use the API
f5_node = "xx-rhwebdev1"         # The F5 node we want to connect to.
with f5_admin.F5Client(None,None,None) as client:
   client.load(f5_node)             # Now we're ready to open a remote connection
   f_qkview = "/var/tmp/" + f5_node + ".qkview"
   f_ucs = "/shared/" + f5_node + ".ucs"
   cmd_01 = "qkview -f " + f_qkview     # take f5 diagnostic snapshop
   cmd_02 = "save /sys ucs " + f_ucs    # take f5 backup
   # Execute the commands one by one:
   for x in [cmd_01,cmd_02]:
       client.ssh_command(client.ssh_connect(), x, "")
