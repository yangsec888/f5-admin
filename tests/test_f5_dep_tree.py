import unittest
from f5_admin.f5_dep_tree import F5DepTree
from os import unlink
from os.path import isfile,isdir,join,dirname,realpath,getsize


class TestF5DepTree(unittest.TestCase):
    def setUp(self):
        print("\nTest F5DepTree Class ...")
        credential = {
            "user_name": "root",
            "user_pass": "password"
        }
        self.client = F5DepTree(credential, 7, False)
        self.client.port = 22
        self.client.cache_config_base = dirname(realpath(__file__))
        self.client.cache_config_dir = self.client.cache_config_base
        self.client.cache_config = self.client.cache_config_dir + "/" + "f5_sample.txt"
        self.client.top_objs=self.client.parse_conf_obj()
        self.client.dep_tree = self.client.build_dep_tree()

    def tearDown(self):
        pass

    def test_load(self):
        self.assertEqual(getsize(self.client.cache_config),211258)
        self.assertEqual(len(list(self.client.top_objs.keys())), 255)

    def test_filter_f5_objs(self):
        self.assertEqual(len(list(self.client.filter_f5_objs(self.client.top_objs,"ltm virtual").keys())), 3)
        self.assertEqual(len(list(self.client.filter_f5_objs(self.client.top_objs,"ltm node").keys())), 4)
        self.assertEqual(len(list(self.client.filter_f5_objs(self.client.top_objs,"asm policy").keys())), 2)

    def test_dep_tree_leaves(self):
        #print "Dep Tree: ", self.client.dep_tree
        self.assertEqual(len(self.client.dep_tree), 255)

    def test_dep_resolv(self):
        node = "ltm virtual virt-svr-sam1"
        result=self.client.dep_resolve(node)
        result.sort()
        self.assertEqual(result, ['ltm policy asm_auto_l7_policy__virt-svr-sam1', 'ltm pool sam-pool-1', 'ltm profile http http-x-forwarded-for', 'net vlan dev_int_vlan703'])


if __name__ == '__main__':
    unittest.main()
