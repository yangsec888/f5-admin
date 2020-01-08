![image](/images/f5_logo.png)
=====================

- [Introduction](#introduction)
- [API Document](#python-docstrings)
  - [Python Docstrings](#python-docstrings)
  - [API Document in HTML](#api-document-in-html)
  - [Read the Source Code](#read-the-source-code)
- [Build Your Own](#build-your-own)
  - [My First F5 Tool](#my-first-f5-tool)
  - [Test Run the Tool](#test-run-the-tool)
  - [Improve the Tool](#improve-the-tool)
- [More API Example](#more-api-example)

---
# Introduction
![image](/images/background_1.png)
=====================
F5 Admin API provides the opportunity to build your own F5 automation tool in Python. Here you can find more information of the API. And the example to build your own tools.

The API was developed with a few idioms in mind:
   1. Keep It Simple
   2. Make It Beautiful
   3. Make It Enjoyable

All future developments would be bound by the above rules.

## Python Docstrings
Python modules are usually documented using docstrings. You can read the module's docstrings from the Python interactive shell, such as below:

```bash
$ python
>>> import f5_admin
>>> help(f5_admin)
Help on package f5_admin:

NAME
    f5_admin

FILE
    /Library/Python/2.7/site-packages/f5_admin/__init__.py

PACKAGE CONTENTS
    f5_asm
    f5_client
    f5_data_group
    f5_dep_tree
    util

CLASSES
    f5_admin.f5_client.F5Client
        f5_admin.f5_asm.F5Asm
        f5_admin.f5_data_group.F5DataGroup

    class F5Asm(f5_admin.f5_client.F5Client)
....
```

## API Document in HTML
You can also download the [API HTML Document](/html.zip). Unzip it under your local drive. Then under your favorite browser to open the index.html page.

## Read the Source Code
Eventually you might also want to check out the API source code under the ['src' directory](/src).

# Build Your Own  
The 'f5_client' class provides the hook for you to access the remote F5 box. Then you can perform your Python fu from there. To start, you want to make sure you have Python 3 in your local machine. And the 'f5' package is already installed in your python environment. Refer to [README](/README.md) for installation instructions.

```bash
$ python -V
Python 3.7.5
$ pip list | grep f5
f5                                     1.1.6 or current version
```

## My First F5 Tool
Copy the following code block in a text editor. Then save it into a file name 'test.py'. Or <a href="/src/bin/test.py" target="_blank">Download it</a> as raw file.
```python
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
```

## Test Run the Tool
Run the 'test' utility in Python. Enter your F5 credential at the prompt. Here is what you will see:
```bash
$ python test.py
Loading cache_config:  /Library/Python/2.7/site-packages/f5_admin-1.0.0-py2.7.egg/f5_admin/conf/xx-rhwebdev1/xx-rhwebdev1.txt
Loading complete
Setting up remote SSH session to host: xx-rhwebdev1
Please enter the F5 user name:
Please enter the F5 password:
Execution on the remote SSH host:  show sys software
Command execution complete.



----------------------------------------------------------

Sys::Software Status

Volume  Slot  Product   Version    Build  Active    Status

----------------------------------------------------------

HD1.1      1   BIG-IP  12.1.3.4    0.0.2     yes  complete

HD1.2      1   BIG-IP    11.6.1  2.0.338      no  complete
...
```

## Improve the Tool
In the real world you want the tool to be both reliable and user friendly as possible. In order to archive the goal, you may end up adding a lot of extra code to the tool.

The improved tool can be found as [f5-run](/src/bin/f5-run) within this package. If you have the package installed already, you can run it like below:

```bash
$ f5-run -n xx-rhwebdev1 -p $F5Pass -c "show sys software"
...
Loading cache_config:  /Library/Python/2.7/site-packages/f5_admin-1.0.0-py2.7.egg/f5_admin/conf/xx-rhwebdev1/xx-rhwebdev1.txt
Loading complete
Total Number of Top Level objects:  267
Setting up remote SSH session to host: xx-rhwebdev1
Execution on the remote SSH host:  tmsh show sys software
Command execution complete.
...

--------------------------------------------------------

Sys::Software Status

Volume  Slot  Product   Version  Build  Active    Status

--------------------------------------------------------

HD1.1      2   BIG-IP  12.1.3.4  0.0.2      no  complete
```

# More API Example
If you want to see another API example, click [here](API2.md)

---
:monkey: $F5Pass - this is the shell environment variable storing my root password :v:
