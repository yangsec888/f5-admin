# !/usr/bin/env python              # Let's build a tool together
import f5_admin                     # First we need to let Python know we're going to use the API
f5_node = "xx-rhwebdev1"         # The F5 node we want to connect to.
f5_command = "show sys software"    # The F5 command we want to run
with f5_admin.F5Client(None,None,None) as client:
   client.load(f5_node)             # Now we're ready to open a remote connection
   result=client.ssh_command(client.ssh_connect(),f5_command,"")
   for line in result:              # line print the F5 command result in the console
       print(line)

# Congratulation. You just build an automation tool with the API!
