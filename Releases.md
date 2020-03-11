[![image](/images/f5_logo.png)](https://github.com/yangsec888/f5-admin)
=====================

- [Current version](#current-version)
- [What's New](#whats-new)
  - [Release 1.1.8](#release-118)
  - [Release 1.1.6](#release-116)
  - [Release 1.1.5](#release-115)
  - [Release 1.1.4](#release-114)
  - [Release 1.1.3](#release-113)
  - [Release 1.1.2](#release-112)
  - [Release 1.0.0](#release-100)
  - [Release 0.0.5](#release-005)
  - [Release 0.0.4](#release-004)
  - [Release 0.0.3](#release-003)
- [Source Code](#source-code)
- [Installation](#installation)
  - [Note](#note)
- [Internal Only](#internal-only)
- [Question](#question)

---


## Current version
The current version of the software: 1.1.6; which is released on: November, 2019. Note the current version require Python 3 runtime environment. Refer to (README)(/README.md) for more details.

This is a simple python API built for F5 security administrators. I call it F5 security admin's DIY Swiss Army knife. I implemented the API in order to make my life more enjoyable and productive.

The API provides a direct hook to the F5 TMOS command line interface from your workstation, by establishing a TTY via SSH connection as the privileged user. Once hooked, the security admin will be able to manipulate F5 running configuration based on the standard TMOS commands. In additional, the security admin can further implement the custom automation procedures in the object-oriented Python programming paradigm.

## What's New:
In this release, the package structure is changed. In addition to the base class F5Client, now we have super class such as F5Asm, F5DataGroup that handle respective challenges within their own name space.

In additional to new features and the bug fixes, additional utilities / executables are added as below:

### Release 1.1.8
- f5-delete: This utility is the opposite of 'f5-put'. It will parse and delete the F5 configuration objects.

### Release 1.1.6
- Source code conversion from [Python 2 to 3](https://docs.python.org/2/library/2to3.html).
- Support [virtualenv](https://docs.python-guide.org/dev/virtualenvs/#virtualenvironments-ref)  

### Release 1.1.5
- f5-resolve: The utility resolve and print out F5 Configuration Object Dependency objects [F5DepTree](/src/f5_dep_tree.py).

### Release 1.1.4
Implement F5 Configuration Object Dependency Tree Resolving Algorithm in class [F5DepTree](/src/f5_dep_tree.py).

### Release 1.1.3
- oom-mon: The utility monitor kernel log for [out-of-memory kill](https://support.f5.com/csp/article/K16786) activity; if found will send email notification.  

### Release 1.1.2
- Additional features are added over minor releases between 1.0.9 and 1.1.2
- f5-runs:     The utility to allow you execute TMSH command bat file from your local workstation
- dsk-chk:     The utility to check F5 file system utilization. It will raise an alarm when any disk partition fill up to 90%.

### Release 1.0.9
- Additional features are added over minor releases between 1.0.0 and 1.0.9
- cert-chk:   The utility to check local F5 cache configuration files for any expiring client ssl cert in the next 30 days.
- dg-sap:   Custom automation utility to setup SAP PI Endpoint Proxy in production environment.
- f5-setup-bacup: Custom automation utility to setup F5 node to be backed daily in production environment.
- f5-install-cert: Custom automation utility to install new certs in the F5 nodes.
- f5-sync:  Custom automation utility to sync F5 node to 'device-group-failover' object in the running configuration.

### Release 1.0.0
- Better documentations, including Sphinx API doc for the project
- Complete unit test for main components i.e. util.py and f5_client.py

### Release 0.0.5
- f5-search:  Fast search operating on all known F5 nodes running configurations in parallel.
- f5-run:     The utility to allow you execute TMSH command from your local workstation
- f5-standby: The utility to send the remote F5 nodes into standby mode.
- asm-get:    The utility to pull in ASM policies from your local workstation
- asm-put:    The utility to upload and / or update the ASM policy from your local workstation.
- gap_vip:    The utility to audit F5 VIP applied policies and produce the list of configuration objects with gaps. Currently audit support:
    - splunk logging gap
    - IP-intelligence policy gap
- gap_client-ssl: The utility to audit F5 client-ssl profile for potential gaps.

### Release 0.0.4
Introduce F5DataGroup class to manage the F5 data group objects.
- f5-put:    The utility to allow you to modify F5 running configuration from your workstation.
- f5-fetch:  The utility to sync the F5 running configuration with your local cache.
- dg-get:    The utility to retrieve F5 data group objects.
- dg-put:    The utility to update /publish F5 data group objects.

### Release 0.0.3
- f5-get:      The utility to allow you to filter out F5 running configuration object from your workstation.

### Release 0.0.2
- f5-backup:      The utility rewritten to allow you to backup F5 node from your workstation.

### Release 0.0.1
Introduce f5_client.py basic class to manage F5

## Source Code
Latest source code can be found in the new home: [Github](https://github.com/yangsec888/f5-admin).

## Installation
Refer to [README](README.md) for the instructions on how to build and install from the software.

### Note
The universal Python package distribution tool will install both the depending libraries and the executables for you. For example, the API executables f5-get and f5_patch resemble the RESTFul get and patch method respectively. The Python distribution package is tested under Python 2.7. A fully working installation example can also be found under the Linux box wmstools01.


## Internal Only
Please keep the tool internally only. Do NOT publish it as it may contain proprietary system information.


## Question?
Please contact [Sam Li](mailto:yangsec888@gmail.com) for any question at
