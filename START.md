[![image](/images/f5_logo.png)](https://github.com/yangsec888/f5-admin)
=====================

- [Introduction](#introduction)
  - [What's F5 Configuration Object](#whats-f5-single-configuration-object)
  - [Where Are the Sample Code](#where-are-the-sample-code)
- [Example 1 - Fetch F5 Configuration](#example-1-fetch-f5-configuration)
- [Example 2 - Filter F5 Object](#example-2-filter-f5-object)
- [Example 3 - Deploy F5 object](#deploy-f5-object)
  - [A) Verify F5 objects](#a-verify-f5-objects)
  - [B) Deploy After Validation](#b-deploy-after-validation)
- [Example 4 - Deploy an ASM Policy](#example-4-deploy-an-asm-policy)
- [Want more?](#want-more)

---

## Introduction
Here you will find information on how to use some custom build utilities in the first hand. Before we start though, I want to review / warm-up on some basic F5 concepts.

### What's F5 Single Configuration Object
You can use the TMOS Shell (tmsh) to define all BIG-IP configuration elements in Single Configuration File or [SCF](https://support.f5.com/csp/article/K13408).  SCF is actually a plain text file with F5 special syntax for configuration definition. All native BIG-IP system configuration elements are defined in various SCFs. In addition, F5 module configuration / underlining OS(Linux) configuration /device trust certs are translated into SCFs and managed by F5. In a nutshell, SCF is the standard abstract configuration layer in F5 world.

Within the SCF, there are composed of F5 objects, I would call them Single Configuration Object (SCO). Examples of F5 SCOs can be found in a simple SCF below:
```
ltm node sam-1  {
    address xx.xx.224.50
}

ltm node sam-2  {
    address xx.xx.224.51
}

ltm pool sam-pool-3  {
    members {
        sam-1:https {
            address xx.xx.224.50
        }
        sam-2:https {
            address xx.xx.224.51
        }
    }
}

ltm virtual virt-svr-sam1  {
    description "test only"
    destination xx.xx.220.70:http
    ip-protocol tcp
    mask 255.255.255.255
    pool sam-pool-3
    source 0.0.0.0/0
    translate-address enabled
    translate-port enabled
    vlans {
        dev_int_vlan703
    }
    vlans-enabled
    vs-index 3
}
```
In the above example SCF, we're building a load balancer for a typical web server cluster behind F5. There are 4 F5 SCOs defined there, confined by the curly brackets. The first and second objects are F5 node; the third object is F5 pool; the last object is F5 virtual server. The configuration file have a [multi-layer structure](TREE.md), where the virtual server object contains the pool object; and the pool object contains node object.  

From a programmer's perspective, the F5 security administrator's job is to build and maintain the F5 SCOs. Of course, the tasks can be easily accomplished by using the standard F5 web GUI. However, F5 Admin API provides a more direct and scalable alternative to get the job done programmatically.

### Where Are the Sample Code
There are some common tools bundled with this Python package. The tools are the best illustration on how we can use the API to manipulate SCFs within the F5 world. The tools can be found under the [source directory](/src/bin/).

In general, you can use the tool command switch "-h" to inquire about its usage, such as below:

```bash
$ f5-fetch -h
...
usage: f5-fetch [-h] [-l] [-n NODE] [-u USER] [-p PASSWORD [PASSWORD ...]]
                [-v] [-a] [-f FILE]

This program will retrieve F5 running configuration for you.

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            (Optional) List of available F5 configuration files
                        under the local cache directory.
  -n NODE, --node NODE  (Optional) Remote F5 hostname or IP address
  -u USER, --user USER  (Optional) F5 box logon user ID. Default to root.
  -p PASSWORD [PASSWORD ...], --password PASSWORD [PASSWORD ...]
                        (Optional) F5 box root password
  -v, --verbose         (Optional) Verbose mode
  -a, --all             (Optional) Fetech all the F5 running configuration in
                        the local cache directory.
  -f FILE, --file FILE  (Optional) File with list of F5 box as program input -
                        to be fetched.

```


## Example 1 - Fetch F5 Configuration
Fetch F5 running configuration file for the first time. It will be placed in your local file system as cache.

```bash
$ sudo f5-fetch -n xx-rhwebdev1 -u sli
Password:
...

Loading cache_config:  /Library/Python/2.7/site-packages/f5-0.0.5-py2.7.egg/f5/conf/xx-rhwebdev1/xx-rhwebdev1.txt
Loading complete
Fetch the running configuration on:  xx-rhwebdev1
Setting up remote SSH session to host: xx-rhwebdev1
Please enter the F5 password:
Execution on the remote SSH host:  list
Command execution complete.

F5 running configuration is saved to file:  /Library/Python/2.7/site-packages/f5-0.0.5-py2.7.egg/f5/conf/xx-rhwebdev1/xx-rhwebdev1.txt
```

## Example 2 - Filter F5 Object
Filter out interesting F5 running configuration objects. This will be done from your command line by working on the cache file:

```bash
$ f5-get -n xx-gtmprd1 -f1 corpdir.mask.com
...
Parsing the f5 running configurations ...
Parsing done.

Total Number of Top Level objects: 210
Filtering F5 objects ...
Filtering done.

Found Total Number of Filtered objects: 2
gtm pool a corpdir.mask.com-int {
 alternate-mode global-availability
 fallback-mode none
 load-balancing-mode topology
 members {
 xx-rhwebprd:/Common/corpdir-http-int {
 member-order 0
 }
 xx-rhwebprd:/Common/corpdir-http-int {
 member-order 1
 }
 }
}
gtm wideip a corpdir-int.glb.mask.com {
 pools {
 corpdir.mask.com-int {
 order 0
 }
 }
}

All done. Bye!
```

## Example 3 - Deploy F5 object
The object(s) could be defined in a configuration file. Then the configuration file can be deployed from your workstation.

Note that when you exam your object definition, please make sure all references are already properly defined / deployed. Or the F5 will throw out the exception during the deployment.  

### A) Verify F5 objects
It's a good idea to test the integrity of your configuration object(s), by using the F5 build-in integrity checker. A dry run example is illustrated below:

```bash
$ f5-put -r -n xx-rhwebdev1 -p MASKED -f f5/src/inc/splunk-log.inc


Execute shell command: sshpass -p MASKED scp -q f5/src/inc/splunk-log.inc root@xx-rhwebdev1:/var/tmp/splunk-log.inc
Parsing the f5 running configurations ...
Parsing done.

Setting up remote SSH session to host: xx-rhwebdev1
Execution on the remote SSH host: tmsh load sys config verify file /var/tmp/splunk-log.inc


Task complete.

Validating system configuration...
 /defaults/asm_base.conf
 /defaults/config_base.conf
 /defaults/ipfix_ie_base.conf
 /defaults/ipfix_ie_f5base.conf
 /defaults/low_profile_base.conf
 /defaults/low_security_base.conf
 /defaults/policy_base.conf
 /defaults/wam_base.conf
 /defaults/analytics_base.conf
 /defaults/apm_base.conf
 /defaults/apm_saml_base.conf
 /defaults/app_template_base.conf
 /defaults/classification_base.conf
 /var/libdata/dpi/conf/classification_update.conf
 /defaults/urlcat_base.conf
 /defaults/daemon.conf
 /defaults/pem_base.conf
 /defaults/profile_base.conf
 /defaults/sandbox_base.conf
 /defaults/security_base.conf
 /defaults/urldb_base.conf
 /usr/share/monitors/base_monitors.conf
 /usr/local/gtm/include/gtm_base_region_isp.conf
 /usr/share/monitors/gtm_base_monitors.conf
Validating configuration...
 /var/tmp/splunk-log.inc
Execution on the remote SSH host: rm -rf /var/tmp/splunk-log.inc


Task complete.


All done. Bye!
```
If you see any error message from the above dry run, you might want to go back to your configuration file. Exam and correct the error before next dry run.

### B) Deploy After Validation
Once the object(s) are properly verified from the above step, it'll be safe to be deployed:
```bash
$ f5-put -n xx-rhwebdev1 -p MASKED -f f5/src/inc/splunk-log.inc



Execute shell command: sshpass -p MASKED scp -q f5/src/inc/splunk-log.inc root@xx-rhwebdev1:/var/tmp/splunk-log.inc
Parsing the f5 running configurations ...
Parsing done.

Setting up remote SSH session to host: xx-rhwebdev1
Execution on the remote SSH host: tmsh load sys config merge file /var/tmp/splunk-log.inc


Task complete.

Loading configuration...
 /var/tmp/splunk-log.inc
Execution on the remote SSH host: tmsh save /sys config partitions all


Task complete.

Saving running configuration...
 /config/bigip.conf
 /config/bigip_base.conf
 /config/bigip_user.conf
Execution on the remote SSH host: rm -rf /var/tmp/splunk-log.inc


Task complete.


All done. Bye!
```

## Example 4 - Deploy an ASM Policy
The ASM policy file should be in the XML format, residing in your local file system. This could be the ASM policy exported from a different F5 node. Or it could be an enhance policy file being pushed back to the same F5 node.

```bash
$ asm_put -n xx-rhwebdev1 -f wordpress_template_08232018.xml

...
Policy name:  wordpress_template
File path:  /var/tmp/wordpress_template_08232018.xml
Setting up remote SSH session to host: xx-rhwebdev1
Please enter the F5 root password:
Execute shell command:  sshpass -p MASKED scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -q wordpress_template_08232018.xml root@xx-rhwebdev1:/var/tmp/wordpress_template_08232018.xml
Execution on the remote SSH host:  tmsh load asm policy wordpress_template overwrite file /var/tmp/wordpress_template_08232018.xml


Task complete.

Execution on the remote SSH host:  tmsh modify asm policy wordpress_template active


Task complete.

Execution on the remote SSH host:  rm -rf /var/tmp/wordpress_template_08232018.xml


Task complete.


All done. Bye!
```

## Want more?
Want to explore more from here? You can find more information of the [API document](/API.md).
