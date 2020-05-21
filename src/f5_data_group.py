
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
import datetime
import re

# F5 Data Group Class
class F5DataGroup(F5Client):
    def __init__(self, credential, timeout, verbose):
        F5Client.__init__(self, credential, timeout, verbose)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        file = self.cache_config_base

    def load(self,node):
        self.node = node.lower()
        if not is_directory(self.cache_config_base + node):
            mkdir(self.cache_config_base + node)
        self.cache_config = self.cache_config_base + node + "/" + node + ".txt"
        print("Loading cache_config: ", self.cache_config)
        # Retrieve a copy of the f5 running config if cache is non-exist
        if not os.path.isfile(self.cache_config):
            self.fetch()
        # Retrieve a copy of the running config if cache is empty
        if os.path.getsize(self.cache_config) == 0:
            self.fetch()
        self.top_objs=self.parse_conf_file(self.cache_config)
        self.load_dgs(self.node)
        print("Loading complete")

    # Load F5 data group stuffs here
    def load_dgs(self,node):
        self.int_dg_objs=self.filter_f5_objs(self.top_objs,"ltm data-group internal")
        self.int_dg_list = [ f.strip().split(" ")[-1] for f in list(self.int_dg_objs.keys()) ]
        self.ext_dg_objs=self.filter_f5_objs(self.top_objs,"ltm data-group external")
        self.ext_dg_list = [ f.strip().split(" ")[-1] for f in list(self.ext_dg_objs.keys()) ]
        self.cache_dg_dir = self.cache_config_base + node + "/ext_dg/"
        if not is_directory(self.cache_dg_dir):
            mkdir(self.cache_dg_dir)
        # proprietary data structure to hold dg info in memory
        self.dgs = {"ext":{}, "int":{}}
        self.load_ext_dg_objs()
        self.load_int_dg_objs()

    # Function to extract datagroup file name from the configuration object
    def search_dg_file_name(self,obj_val):
        for line in obj_val:
            if re.match(r'    external-file-name ', line):
                return line.split('external-file-name')[1]
        return ""

    # Function to extract VIP destination ip
    def search_dg_type(self,obj_val):
        for line in obj_val:
            if re.match(r'    type ', line):
                return line.split('type')[1]
        return ""

    # Function to Initialize external data group, the goal is to load external data
    # group into data structure: dgs[int|ext][dg_name][key]
    def load_ext_dg_objs(self):
        if self.verbose:
            print("Loading external data group into memory on F5 node: ", self.node)
        #for x in ext_dg_list:
        for x in list(self.ext_dg_objs.keys()):
            dg_name = x.strip().split(" ")[-1]
            dg_file_name = self.search_dg_file_name(self.ext_dg_objs[x])
            cache_dg_file = self.cache_dg_dir + dg_name + ".txt"
            if not is_file(cache_dg_file):
                print("Retrieve the external data group file: ", x)
                contents = self.fetch_ext_dg(dg_file_name,cache_dg_file)
            if is_file(cache_dg_file):
                my_dgs=self.parse_ext_dg_file(cache_dg_file)
                if my_dgs != None:
                    self.dgs["ext"][dg_name]=my_dgs

    # Function to Initialize internal data group, the goal is to load internal data
    # group into data structure: dgs[int|ext][dg_name][key]
    def load_int_dg_objs(self):
        if self.verbose:
            print("Loading internl data group into memory on F5 node: ", self.node)
        #for x in ext_dg_list:
        for x in list(self.int_dg_objs.keys()):
            dg_name = x.strip().split(" ")[-1]
            self.dgs["int"][dg_name]=self.int_dg_objs[x]

    # Retrieve external data group file
    def fetch_ext_dg(self,dg_file_name, cache_dg_file):
        today = datetime.date.today().strftime('%m%d%Y')
        file = cache_dg_file.replace(".txt","") + "." + today
        p_dg=re.compile(r'^.*\_\d+\_\d+$', re.M|re.I)
        if self.verbose:
            print("Retrieve the external data group file: ", dg_file_name)
        conn = self.ssh_connect()
        cmd01 = "find / -name *" + dg_file_name.strip() + "*"
        files = self.ssh_command(conn,cmd01,"")
        dg_files = [f for f in files if p_dg.match(f.rstrip())]
        if len(dg_files) == 0:
            print("Error retrieving external data group file: ",dg_file_name)
            print("dg_files: ", dg_files)
            conn.close()
            return None
            #exit(1)
        if self.verbose:
            print("dg_files: ",dg_files)
        dg_file = self.dg_select(dg_files, conn) # choose the most recent one
        if self.verbose:
            print("Found dg file: ", dg_file)
        cmd02 = "cat " + dg_file
        contents = self.ssh_command(conn,cmd02,"")
        contents_clean = [f.rstrip() for f in contents] # remove new line char
        conn.close()
        if is_file(cache_dg_file):
            unlink(cache_dg_file)
        if list_to_file(contents_clean,file):
            print("Fetch file success:", file)
            symlink(file, cache_dg_file)
            return True
        else:
            print("Fetch file fail: ", cache_dg_file)
            return False

    # Select the latest modified dg file base on the timestamp
    def dg_select(self,dg_files,conn):
        if len(dg_files)==1:
            return dg_files[0].rstrip()
        dg = dg_files[0]
        for f in dg_files:
            if self.dg_modify_time(f.rstrip(),conn) > self.dg_modify_time(dg,conn):
                dg = f.rstrip()
        return dg

    # Obtain dg modify time stamp
    def dg_modify_time(self,dg_file,conn):
        timestamp_command = "stat " + dg_file
        outputs = self.ssh_command(conn, timestamp_command, "")
        for x in outputs:
            if "Modify: " in x:
                return x.split("Modify: ")[1]

    # parsing F5 ext data group file in
    def parse_ext_dg_file(self,ext_dg_file):
        dict={}
        with open(ext_dg_file, 'r') as f:
            line=f.readline()
            while line:
                entry = line.replace(",\n","").split(":=")
                #print "entry:",entry
                if len(entry)>1:
                    dict.update({entry[0].strip(): entry[1].strip()})
                else:         # protection in case delimiter is not ' := '
                    dict.update({entry[0].strip(): ""})
                line=f.readline()
        #print "dict:",dict
        return dict

    # Function to extract external data group file name
    def search_ext_dg_file_name(self,obj_val):
        for line in obj_val:
            if re.match(r'    external-file-name ', line):
                return line.split('external-file-name')[1].strip()
        return ""

    # print external data group content in plain text from dgs data structure
    def print_ext_dg(self,ext_dg_name):
        if self.dgs['ext'][ext_dg_name]:
            for key,val in self.dgs['ext'][ext_dg_name].items():
                print(key, ":=", val, ",")
