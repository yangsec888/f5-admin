
################################################################################
#  Python API to manipulate the remote F5 box running configuration
#    via SSH port 22 as privileged user
#
################################################################################
#
# Author: Sam Li 
#
################################################################################
from f5_admin import F5Client
from .util import *
import os
from os import listdir,unlink,symlink,mkdir
from os.path import isfile,isdir,join,dirname,realpath,getsize
import datetime
import re

# Dependency tree node data structure
# Refer to the article for reference: https://www.electricmonk.nl/log/2008/08/07/dependency-resolving-algorithm/
class Node:
    def __init__(self, name):
        self.name = name
        self.edges = []

    def addEdge(self, node_name):
        if node_name not in self.edges:
            self.edges.append(node_name)

# Class to implement F5 Configuration Object Dependency Resovling Algorithm
class F5DepTree(F5Client):
    def __init__(self, credential, timeout, verbose):
        F5Client.__init__(self, credential, timeout, verbose)
        #self.load(self, node)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        #os.unlink(file)
        file = self.cache_config_base

    # Overloading F5Client 'load' method
    def load(self,node):
        if not is_valid_hostname(node):        # F5 node validation check
            exit(1)
        self.node = node.lower().split('.')[0]
        self.cache_config_dir = self.cache_config_base + self.node
        if not is_directory(self.cache_config_dir):
            mkdir(self.cache_config_dir)
        self.cache_config = self.cache_config_dir + "/" + self.node + ".txt"
        print("Loading cache_config: ", self.cache_config)
        # Retrieve a copy of the running config if cache is non-exist
        if not isfile(self.cache_config):
            self.fetch()
        # Retrieve a copy of the running config if cache is empty
        if getsize(self.cache_config) == 0:
            self.fetch()
        self.top_objs=self.parse_conf_file(self.cache_config)
        self.dep_tree = self.build_dep_tree()
        print("Loading complete")

    # Build the dependency tree based on the existing F5 configuration objects
    def build_dep_tree(self):
        if self.verbose:
            print(list(self.top_objs.keys()))
            print("Total object count: ", len(list(self.top_objs.keys())))
        # first, use dictionary comprehension to create the basic tree data structure
        dep_tree = { key:Node(key) for key in list(self.top_objs.keys()) }
        # secondary, walk through all nodes in the basic tree structure one by one, and build node relationships / tree branches
        for node in list(dep_tree.values()):
            self.build_tree_branches(node)
        return dep_tree

    # Build tree branches / node relationships
    def build_tree_branches(self, node):
        if "ltm virtual " in node.name:                  # case for load balancer nodes 'VIPs'
            self.build_tree_branches_vip(node)
        elif "security firewall policy " in node.name:   # case for AFM firewall policy
            self.build_tree_branches_afm_policy(node)
        elif "security firewall rule-list " in node.name: # case for AFM rule-list
            self.build_tree_branches_afm_rules(node)
        return None

    # parse vip single configuration object, then extract and build the relationships
    def build_tree_branches_vip(self, node):
        for entry in self.top_objs[node.name]:
            if "pool " in entry:   # add dependendant pool
                pool_node_name = "ltm pool " + entry.split(" ")[-1]
                node.addEdge(pool_node_name)
            if "ip-intelligence-policy " in entry:    # add dependendant ip-intel policy
                pool_node_name = "security ip-intelligence policy " + entry.split(" ")[-1]
                if pool_node_name in list(self.top_objs.keys()):
                    node.addEdge(pool_node_name)
            if "security-log-profiles {" in entry: # add dependendant security log profile
                security_log_profiles = self.parse_obj_one_indention("security-log-profiles {", self.top_objs[node.name])
                for entry in security_log_profiles:
                    pool_node_name = "security log profile " + entry.split(" ")[-1]
                    if pool_node_name in list(self.top_objs.keys()):
                        node.addEdge(pool_node_name)
            if "fw-enforced-policy " in entry: # add dependendant fw-policy
                pool_node_name = "security firewall policy " + entry.split(" ")[-1]
                if pool_node_name in list(self.top_objs.keys()):
                    node.addEdge(pool_node_name)
            if "rules {" in entry: # add dependendant irule
                irules = self.parse_obj_one_indention("rules {", self.top_objs[node.name])
                for entry in irules:
                    pool_node_name = "ltm rule " + entry.split(" ")[-1]
                    if pool_node_name in list(self.top_objs.keys()):
                        node.addEdge(pool_node_name)
            if "policies {" in entry: # add dependendant asm policy
                policies = self.parse_obj_one_indention("policies {", self.top_objs[node.name])
                for entry in policies:
                    pool_node_name = "ltm policy " + entry.strip().split(" ")[0]
                    if pool_node_name in list(self.top_objs.keys()):
                        node.addEdge(pool_node_name)
            if "vlans {" in entry: # add dependendant vlans
                vlans = self.parse_obj_one_indention("vlans {", self.top_objs[node.name])
                for entry in vlans:
                    pool_node_name = "net vlan " + entry.split(" ")[-1]
                    if pool_node_name in list(self.top_objs.keys()):
                        node.addEdge(pool_node_name)
            if "profiles {" in entry: # add dependendant profiles
                profiles = self.parse_obj_two_indention("profiles {", self.top_objs[node.name])
                if self.verbose:
                    print("Found dependendant ltm profiles: ", profiles)
                for entry in profiles:
                    pool_node_name = self.ltm_profile_lookup(entry)
                    if pool_node_name in list(self.top_objs.keys()):
                        if self.verbose:
                            print("Add dependendant ltm profile: ", pool_node_name)
                        node.addEdge(pool_node_name)
        return None

    # parse afm single configuration object, then extract and build the relationships
    def build_tree_branches_afm_policy(self, node):
        for entry in self.top_objs[node.name]:
            if " rule-list " in entry:       # add dependant rule list
                pool_node_name = "security firewall rule-list " + entry.split(' ')[-1]
                if pool_node_name in list(self.top_objs.keys()):
                    node.addEdge(pool_node_name)
            if "address-lists {" in entry:   # add dependant address-lists
                addr_lists = self.parse_obj_one_indention("address-lists {", self.top_objs[node.name])
                for addr in addr_lists:
                    pool_node_name_1 = "security firewall address-list " + addr.split(" ")[-1]
                    pool_node_name_2 = "security shared-objects address-list " + addr.split(" ")[-1]
                    if pool_node_name_1 in list(self.top_objs.keys()):
                        node.addEdge(pool_node_name_1)
                    if pool_node_name_2 in list(self.top_objs.keys()):
                        node.addEdge(pool_node_name_2)
            if "fqdns {" in entry:          # add dependant fqdn list
                fqdns = self.parse_obj_one_indention("fqdns {", self.top_objs[node.name])
                for fqdn in fqdns:
                    pool_node_name = "security firewall fqdn-entity " + fqdn.split(" ")[-3]
                    if pool_node_name in list(self.top_objs.keys()):
                        node.addEdge(pool_node_name)
            if "port-lists {" in entry:   # add dependant port-lists
                port_lists = self.parse_obj_one_indention("port-lists {", self.top_objs[node.name])
                for port in port_lists:
                    pool_node_name = "security firewall port-list " + port.split(" ")[-1]
                    if pool_node_name in list(self.top_objs.keys()):
                        node.addEdge(pool_node_name)
            if "vlans {" in entry:   # add dependant vlans
                vlan_lists = self.parse_obj_one_indention("vlans {", self.top_objs[node.name])
                for vlan in vlan_lists:
                    pool_node_name = "net vlan " + vlan.split(" ")[-1]
                    if pool_node_name in list(self.top_objs.keys()):
                        node.addEdge(pool_node_name)
        return None

    # Parse afm single configuration object such as 'security firewall rule-list NetIQ-PRD-IDP-ADM ',
    # then extract the content and build the relationships
    def build_tree_branches_afm_rules(self, node):
        for entry in self.top_objs[node.name]:
            if "address-lists {" in entry:   # add dependendant address-lists
                addr_lists = self.parse_obj_one_indention("address-lists {", self.top_objs[node.name])
                for addr in addr_lists:
                    pool_node_name_1 = "security firewall address-list " + addr.split(" ")[-1]
                    pool_node_name_2 = "security shared-objects address-list " + addr.split(" ")[-1]
                    if pool_node_name_1 in list(self.top_objs.keys()):
                        node.addEdge(pool_node_name_1)
                    if pool_node_name_2 in list(self.top_objs.keys()):
                        node.addEdge(pool_node_name_2)
            if "port-lists {" in entry:   # add dependendant port-lists
                port_lists = self.parse_obj_one_indention("port-lists {", self.top_objs[node.name])
                for port in port_lists:
                    pool_node_name = "security firewall port-list " + port.split(" ")[-1]
                    if pool_node_name in list(self.top_objs.keys()):
                        node.addEdge(pool_node_name)
        return None

    # Parse a F5 Single Configuration Object (one level curly bracket indention ); then return element list.
    # example input:
    # ['    destination 10.107.221.128:http', '    ip-intelligence-policy ip-intelligence', '    ip-protocol tcp', '    mask 255.255.255.255', '    profiles {', '        http-x-forwarded-for { }', '        tcp { }', '    }', '    rules {', '        okta-http-https', '    }', '    security-log-profiles {', '        splunk-logging', '        splunk-logging_local', '    }', '    source 0.0.0.0/0', '    translate-address enabled', '    translate-port enabled', '    vlans {', '        dev_int_vlan703', '        dev_web_srvr_422', '    }', '    vlans-enabled', '    vs-index 196']
    #
    # example output: ['splunk-logging', 'splunk-logging_local']
    def parse_obj_one_indention(self, pattern_string, input_obj):
        p_empty = re.compile(r'^(\w+\s)+.*\{\s\}$',re.M|re.I) # match empty configuration object
        p_end = re.compile(r'^\s+}$', re.M|re.I) # match end of configuration object
        recording=False
        if self.verbose:
           print("Parsing the F5 Single Configuration Object within one indention: ", pattern_string, input_obj)
        output_obj = []
        for x in input_obj:
            if self.verbose:
                print("Parsing line:",x)
            if pattern_string in x:
                recording=True
                if p_empty.match(x):
                    break
                else:
                    continue
            if recording and p_end.match(x):
                recording = False
                if self.verbose:
                    print("Ending found: ", x)
                break
            if recording:
                if self.verbose:
                    print("Adding object: ", x)
                output_obj.append(x)
                continue
        if self.verbose:
            print("My output objects: ", output_obj)
        return output_obj

    # Parse a F5 Single Configuration Object (two level curly bracket indention ); then return element list.
    # Example input: ['    destination 10.107.224.66:webcache', '    disabled', '    ip-intelligence-policy ip-intelligence', '    ip-protocol tcp', '    mask 255.255.255.255', '    pool app-apidev-api-services', '    profiles {', '        http-x-forwarded-for { }', '        tcp { }', '    }', '    security-log-profiles {', '        splunk-logging', '        splunk-logging_local', '    }', '    source 0.0.0.0/0', '    translate-address enabled', '    translate-port enabled', '    vlans {', '        dev_int_vlan703', '    }', '    vlans-enabled', '    vs-index 43']
    # Example output: ['http-x-forwarded-for','tcp']
    #
    # Note 10232019, SL:
    #  The reverse algo is good for now. In the future it might need additional work to check the
    #  inner indention
    #
    def parse_obj_two_indention(self, pattern_string, input_obj):
        p_empty = re.compile(r'^(\w+\s)+.*\{\s\}$',re.M|re.I) # match empty configuration object
        p_end = re.compile(r'^\s+}$', re.M|re.I) # match end of configuration object
        recording=False
        recording_obj = []
        if self.verbose:
           print("Parsing the F5 Single Configuration Object within two indention: ", input_obj)
        for x in input_obj:
            if self.verbose:
                print("Parsing line:",x)
            if pattern_string in x:
                recording=True
                recording_obj.append(x)
                continue
            if recording:
                recording_obj.append(x)
            if p_end.match(x):
                if self.count_bracket(recording_obj, "{") == 0:
                    continue # skip
                if self.count_bracket(recording_obj, "{") > self.count_bracket(recording_obj, "}"):
                    continue
                else:
                    recording=False
                    break
        if self.verbose:
            print("Recording object within two indention: ", recording_obj)
        if len(recording_obj) > 0:
            output_obj=[a.strip().split(' ')[0] for a in recording_obj]
        if self.verbose:
            print("Parsing single configuration object within two indent output: ", output_obj)
        if len(output_obj) >= 2:      # Trim off the enclosure
            output_obj.pop()
            return output_obj[1:]
        else:
            return []

    # ltm profile lookup method
    # example input: 'http-x-forwarded-for', 'tcp'
    # example output:
    def ltm_profile_lookup(self, name):
        if self.verbose:
            print("ltm profile lookup for: ", name)
        for item in list(self.top_objs.keys()):
            if "ltm profile" in item and name in item:
                return item
        return None

    # Walking through the F5 configuration dependency tree data structure
    def dep_resolve(self, node_name):
        try:
            if 'resolved' not in globals():
                resolved={}
            if self.verbose:
                print("Walking through node name: ", node_name)
            for key in self.dep_tree[node_name].edges:
                if key not in list(resolved.keys()):
                    resolved.update({key: True})
                    self.dep_resolve(key)
                else:
                    raise Exception('Circular reference detected: %s -> %s' % (self.dep_tree[node_name], self.dep_tree[key]))
        except Exception as e:
            print('F5 configuration dependency resolving failure:', e)
            raise
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        else:
            if self.verbose:
                print(list(resolved.keys()))
        finally:
            return list(resolved.keys())
