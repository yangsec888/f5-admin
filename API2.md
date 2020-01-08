![image](/images/f5_logo.png)
=====================

- [Next API Usage Example](#next-api-usage-example)
  - [Backing Up Configuration Data](#backing-up-configuration-data)
  - [Generating Diagnostic Data](#generating-diagnostic-data)
- [Our Example Source Code](#our-example-source-code)
  - [Test Run the Tool](#test-run-the-tool)
  - [Improve the Tool](#improve-the-tool)
  - [Contact for Help](#contact-for-help)
- [More API Example](#more-api-example)

---

# Next API Usage Example  
In this example, we're going to automate the regular F5 backup chores:
a) Automate the F5 configuration data backup to user configuration set archive (UCS);
b) Automate generating diagnostic data in case of F5 Tech Support (QkView).

## Backing Up Configuration Data
It's important to backup the F5 system in the regular basis. In additional to routine backup, it is also a requirement to backup the system before we upgrade or patch the F5 system. Fortunately F5 provides the native command to facilitate the task. Although [the procedures](https://support.f5.com/csp/article/K13132#BackTMSH) can be performed via F5 web GUI,  it's far more easier to do it directly under 'tmsh' by using the following commands:

```bash
tmsh
save /sys ucs <path/to/UCS>
# Then copy the .ucs file to another system.
```

## Generating Diagnostic Data
In additional to the UCS archive, it's also a requirement to collect diagnostic system data in the ad-hoc situation, in case we need to contact F5 Tech Support for further assistance. Fortunately, F5 provides the standard data collection utility 'qkview' for the task. The qkview utility is an executable program that generates machine-readable (XML) diagnostic data and combines the data into a single compressed Tape ARchive (TAR) format file. Again [the procedures](https://support.f5.com/csp/article/K12878#options) can be performed via F5 web GUI, however it may be easier to do it directly under 'tmsh' by using the following commands:

```bash
tmsh
qkview -f <path/to/QkView>
# Then copy the .qkview file to another system.
```

# Our Example Source Code
Copy the following code block in a text editor. Then save it into a file name 'test2.py'. Or <a href="/src/bin/test2.py" target="_blank">Download it</a> as raw file.
```python
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
```

## Test Run the Tool
Run the 'test2' utility in Python. Enter your F5 credential at the prompt. Here is what you will see:
```bash
$ python src/bin/test2.py
Loading cache_config:  /Library/Python/2.7/site-packages/f5_admin-1.0.3-py2.7.egg/f5_admin/conf/xx-rhwebdev1/xx-rhwebdev1.txt
Loading complete
Setting up remote SSH session to host: xx-rhwebdev1
Please enter the F5 user name: sli
Please enter the F5 password:
Execution on the remote SSH host:  qkview -f /var/tmp/xx-rhwebdev1.qkview
Command execution complete.

Setting up remote SSH session to host: xx-rhwebdev1
Execution on the remote SSH host:  save /sys ucs /shared/xx-rhwebdev1.ucs
Command execution complete.
```

## Improve the Tool
In the real world you want the tool to be both reliable and user friendly as possible. In order to archive the goal, you may end up adding a lot of extra code to the tool.

The improved tool can be found as [f5-backup](/src/bin/f5-backup) within this package. If you have the package installed already, you can run it like below:

```bash
$ f5-backup -n xx-rhwebdev1 -p $F5Pass
...

```
## Contact for Help
Now you should have a good ideal how the API work. It may be the time for you to start building out your F5 tool by yourself. If you need help during the process, please feel free to contact [me](mailto:yangsec888@gmail.com)

# More API Example
If you want to see another API example, click [here](TREE.md)

---
:monkey: $F5Pass - this is the shell environment variable storing my root password :v:
