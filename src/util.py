
################################################################################
#  Python API to manipulate the remote F5 box running configuration
#    via SSH port 22 as privileged user
#
################################################################################
#
# Author: Sam Li 
#
################################################################################
import re
import socket
import os


# check if it's a valid directory
def is_directory(dir_name):
    return os.path.exists(dir_name) and os.path.isdir(dir_name)

# check if it's a valid file
def is_file(file_name):
    return os.path.isfile(file_name)

# converting file rows to a list, one row at a time
def file_to_list(file):
    comment_pattern = re.compile('^#|^\s+#')
    my_list=[]
    with open(file, 'r') as f1:
        line = f1.readline().strip()
        while line:
            if comment_pattern.match(line):
                next
            else:
                my_list.append(line)
            line =  f1.readline().strip()
    f1.close()
    return my_list

# converting a list to a file, one row at a time
def list_to_file(list,file):
    try:
        with open(file, 'w') as f1:
            for x in list:
                f1.write(x + "\n")
        f1.close()
        return True
    except Exception as e:
        print("Error: ", e)
        return False

# Python: Loop through all nested key-value pairs created by xmltodict,
#   credit to Tadhg McDonald-Jensen in stackoverflow
def traverse(obj, prev_path = "obj", path_repr = "{}[{!r}]".format):
    if isinstance(obj,dict):
        it = list(obj.items())
    elif isinstance(obj,list):
        it = enumerate(obj)
    else:
        yield prev_path,obj
        return
    for k,v in it:
        for data in traverse(v, path_repr(prev_path,k), path_repr):
            yield data

# DNS record lookup, return list of IPs
def host_to_ips(hostname):
    ip_list = []
    try:
        ais = socket.getaddrinfo(hostname, None)
        for result in ais:
            #print (result[4][0])
            ip_list.append(result[-1][0])
        return ip_list
    except Exception as e:
        print("Error: ",e, "Unable to resolve hostname: ",hostname)
        return None

# Check if it's valid hostname
def is_valid_hostname(hostname):
    ips = host_to_ips(hostname)
    if ips == None:
        return False
    elif len(ips) > 0:
        return True
    else:
        return False

# Processing credential based on user input case #1
def set_credential_1(id, *args):
    # setup F5 connection string when args.password is provided as user input
    if args:
        if id:
            credential = {
                "user_name": str(id).strip(),
                "user_pass": ' '.join(args)
            }
        else:
            credential = {
                "user_name": "root",
                "user_pass": ' '.join(args)
            }
    return credential

# Processing credential based on user input case #2
def set_credential_2(id):
    # setup F5 connection string when args.password is NOT provided as user input
    if id:
        credential = {
            "user_name": str(id).strip(),
            "user_pass": None
        }
    else:
        credential=None
    return credential
