# !/usr/bin/env python              # F5DepTree Test Example
import f5_admin                     # First we need to let Python know we're going to use the API
f5_node = "xx-rhwebdev1"           # The F5 node we want to connect to.
with f5_admin.F5DepTree(None,None,None) as client:
    client.load(f5_node)
    #for node in client.dep_tree.values():
    #    print node.name, node.edges
    conf_obj_name = "ltm virtual cart-dev.mask.com-ext-ssl"
    result = client.dep_resolve(conf_obj_name)
    print(("Resolving configuration dependency on ", f5_node, 'for object:', conf_obj_name))
    print(result)
