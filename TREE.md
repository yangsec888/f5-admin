[![image](/images/f5_logo.png)](https://github.com/yangsec888/f5-admin)
=====================

- [Introduction](#introduction)
  - [What's F5 Configuration Object](#whats-f5-configuration-object-dependency-tree-resolving-algorithm)
  - [More Read](#more-read)
- [Example 1](#example-1-resolving-ltm-configuration-dependency)
- [Example 2](#example-2-resolving-afm-configuration-dependency)


---

## Introduction
F5 configuration has a very complicate multiple-layer structure. The best way to think about that, it's an upside-down 30-foot big tree, with branches / sub-branches and leaves all over the place. Something like the picture below.

![image](/images/dep_graph1.png)
=====================

### What's F5 Configuration Object Dependency Tree Resolving Algorithm
The [F5 Configuration Object Dependency Tree Resolving algorithm](https://github.com/yangsec888/f5-admin/blob/master/src/f5_dep_tree.py), is a custom algorithm implemented by [Sam Li](https://www.linkedin.com/in/yangli8/). The goal is to identify and manage the complicate dependencies between a very large pool of F5 single configuration object efficiently.

The algorithm is based on [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory#Computer_science), and the previous Python implementation from others, such as [Ferry Boender](https://www.electricmonk.nl/docs/dependency_resolving_algorithm/dependency_resolving_algorithm.html#copyright-license).  


### Algorithm Improvements
In the data structure implementation, I keep the basic node structure. However, the tree structure are different in the following:
- Build out the whole tree structure by using Python dictionary (vs. list). In theory, this may improve both computing speed - O(1) vs O(n),  and the node retrieving flexibility of the algorithm.
- Build the edges using node name instead of whole node. This simplify the resolving lookup process, and reduce the complexity of tree structure.
- Simplify 'Circular reference check' by using existing global variable 'resolved' .

In the algorithm implementation, the basic ideas are still the same. However, there are many additions unique in our case:
- Extending the [F5Client](https://github.com/yangsec888/f5-admin/blob/master/src/f5_client.py) class;
- Build out the whole tree structure;
- Automating the tree node loading process;
- Additional sanity checks and better error handlings.

Overall, with an improvement of data structures and other implementation advantages above, there comes up with a more mature and efficient algorithm.

### More Read
You can find better explanation of the concepts from [Ferry Boender](https://www.electricmonk.nl/docs/dependency_resolving_algorithm/dependency_resolving_algorithm.html#copyright-license) work.

## Example 1 - Resolving LTM Configuration Dependency
Assuming you have this python package installed, and have the access to the F5 configuration file sample. Copy the following code block in a text editor. Then save it into a file name 'test3.py'. Or <a href="/src/bin/test3.py" target="_blank">Download it</a> as raw file.

```python
# !/usr/bin/env python              # F5DepTree Test Example
import f5_admin                     # First we need to let Python know we're going to use the API
f5_node = "xx-dl4prd1"           # The F5 node we want to connect to.
with f5_admin.F5DepTree(None,None,None) as client:
    client.load(f5_node)
    conf_obj_name = "ltm virtual Forward_App_Servers"
    result = client.dep_resolve(conf_obj_name)
    print "Resolving configuration dependency on ", f5_node, 'for object:', conf_obj_name
    print result
```
Then you should be able to run the following code to resolve the configuration dependency for a LTM object 'Forward_App_Servers':

```bash
$ python src/bin/test3.py
Loading cache_config:  /Library/Python/2.7/site-packages/f5_admin/conf/xx-dl4prd1/xx-dl4prd1.txt
Loading complete
Resolving configuration dependency on  xx-dl4prd1 for object: ltm virtual Forward_App_Servers
['security log profile splunk-logging_local', 'security log profile splunk-logging', 'ltm profile fastl4 ftps_fastL4', 'net vlan DL4-prd-int-vlan752']
```

## Example 2 - Resolving AFM configuration Dependency
TBD
