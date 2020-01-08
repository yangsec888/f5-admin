import unittest
from f5_admin.util import *
import os
import re
import socket

test_host="www.google.com"

class TestUtil(unittest.TestCase):

    def setUp(self):
        print("\nTest general utility functions (util.py) ...")

    def test_is_file(self):
        test_file = """\
        This is a test file
        """
        with open(".test.txt","w") as f:
            f.write(test_file)
        try:
            self.assertEqual(True,is_file(".test.txt"))
        finally:
            os.unlink(".test.txt")

    def test_is_directory(self):
        os.mkdir("foo") # create foo sub-directory
        try:
            self.assertEqual(True,is_directory("foo"))
        finally:
            os.rmdir("foo")

    def test_list_to_file(self):
        test_list = list("abcdefg")
        try:
            list_to_file(test_list,"foo")
            self.assertEqual(True,is_file("foo"))
        finally:
            os.unlink("foo")

    def test_is_valid_hostname(self):
        self.assertEqual(True,is_valid_hostname(test_host))

    def test_host_to_ips(self):
        ip=re.compile("\d+.\d+.\d+.\d+.")
        ips=host_to_ips(test_host)
        for x in ips:
            self.assertRegex(x,ip,msg="Test if it's valid IP address")

if __name__ == '__main__':
    unittest.main()
