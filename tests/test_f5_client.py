import unittest
from f5_admin.f5_client import F5Client
from os import unlink
from os.path import isfile,isdir,join,dirname,realpath,getsize


class TestF5Client(unittest.TestCase):
    def setUp(self):
        print("\nTest F5Client Class ...")
        credential = {
            "user_name": "root",
            "user_pass": "password"
        }
        self.client = F5Client(credential, 7, False)
        self.client.port = 22
        self.client.cache_config_base = dirname(realpath(__file__))
        self.client.cache_config_dir = self.client.cache_config_base
        self.client.cache_config = self.client.cache_config_dir + "/" + "f5_sample.txt"
        self.client.top_objs=self.client.parse_conf_obj()

    def tearDown(self):
        pass

    def test_load(self):
        self.assertEqual(getsize(self.client.cache_config),211258)
        self.assertEqual(len(list(self.client.top_objs.keys())), 255)

    def test_filter_f5_objs(self):
        self.assertEqual(len(list(self.client.filter_f5_objs(self.client.top_objs,"ltm virtual").keys())), 3)
        self.assertEqual(len(list(self.client.filter_f5_objs(self.client.top_objs,"ltm node").keys())), 4)
        self.assertEqual(len(list(self.client.filter_f5_objs(self.client.top_objs,"asm policy").keys())), 2)

    def test_pattern_filter_f5_objs(self):
        self.assertEqual(len(list(self.client.pattern_filter_f5_objs(self.client.top_objs,"auth\sldap\ssystem\-auth").keys())), 1)

    def test_write_obj(self):
        test_file = self.client.cache_config = self.client.cache_config_dir + "/" + "test.txt"
        key = "ltm virtual Outbound_FTP"
        val = ['    description "Allowed Outbound FTP based AFM."', '    destination 0.0.0.0:ftp', '    fw-enforced-policy Outbound_FTP', '    ip-protocol tcp', '    mask any', '    pool sam-pool-3', '    profiles {', '        tcp { }', '    }', '    security-log-profiles {', '        splunk-logging', '    }', '    source 0.0.0.0/0', '    source-address-translation {', '        pool Default-Web-Sevrer-SNAT-Pool', '        type snat', '    }', '    translate-address enabled', '    translate-port enabled', '    vs-index 2']
        self.client.write_obj(key,val,test_file)
        self.assertEqual(getsize(test_file),482)
        unlink(test_file)

    def test_search_desc(self):
        val = ['    description "Allowed Outbound FTP based AFM."', '    destination 0.0.0.0:ftp', '    fw-enforced-policy Outbound_FTP', '    ip-protocol tcp', '    mask any', '    pool sam-pool-3', '    profiles {', '        tcp { }', '    }', '    security-log-profiles {', '        splunk-logging', '    }', '    source 0.0.0.0/0', '    source-address-translation {', '        pool Default-Web-Sevrer-SNAT-Pool', '        type snat', '    }', '    translate-address enabled', '    translate-port enabled', '    vs-index 2']
        self.assertEqual(self.client.search_desc(val),'"Allowed Outbound FTP based AFM."')

    def test_search_vip(self):
        val = ['    description "test only"\n', '    destination 10.106.220.50:http\n', '    ip-protocol tcp\n', '    mask 255.255.255.255\n', '    policies {\n', '        asm_auto_l7_policy__virt-svr-sam1 { }\n', '    }\n', '    pool sam-pool-1\n', '    profiles {\n', '        ASM_RHWeb_Base_ASM_Policy { }\n', '        http-x-forwarded-for { }\n', '        tcp { }\n', '        websecurity { }\n', '    }\n', '    security-log-profiles {\n', '        splunk-logging\n', '        splunk-logging_local\n', '    }\n', '    source 0.0.0.0/0\n', '    translate-address enabled\n', '    translate-port enabled\n', '    vlans {\n', '        dev_int_vlan703\n', '    }\n', '    vlans-enabled\n', '    vs-index 3\n']
        self.assertEqual(self.client.search_vip(val),'10.106.220.50')

    def test_search_cert_in_client_ssl_profile(self):
        val = ['    app-service none', '    cert wildcard.dev.mask.com-clientssl.crt', '    cert-key-chain {', '        wildcard_wildcard {', '            cert wildcard.dev.mask.com-clientssl.crt', '            chain wildcard.dev.mask.com-clientssl.crt', '            key wildcard.dev.mask.com-clientssl.key', '        }', '    }', '    chain wildcard.dev.mask.com-clientssl.crt', '    defaults-from clientssl', '    destination-ip-blacklist none', '    destination-ip-whitelist none', '    hostname-blacklist none', '    hostname-whitelist none', '    inherit-certkeychain false', '    key wildcard.dev.mask.com-clientssl.key', '    passphrase none', '    source-ip-blacklist none', '    source-ip-whitelist none']
        self.assertEqual(self.client.search_cert_in_client_ssl_profile(val),'wildcard.dev.mask.com-clientssl.crt')

    def test_search_client_ssl(self):
        val = ['    description "sam li test"', '    destination 10.106.220.50:https', '    ip-protocol tcp', '    mask 255.255.255.255', '    profiles {', '        http-x-forwarded-for { }', '        serverssl-insecure-compatible {', '            context serverside', '        }', '        tcp { }', '        wildcard.dev.mask.com-clientssl {', '            context clientside', '        }', '    }', '    rules {', '        niq-security-block', '    }', '    security-log-profiles {', '        splunk-logging', '        splunk-logging_local', '    }', '    source 0.0.0.0/0', '    translate-address enabled', '    translate-port enabled', '    vlans {', '        Vlan422-WebSrvr-10.106.222.x', '        dev_int_vlan703', '    }', '    vlans-enabled', '    vs-index 4']
        self.assertEqual(self.client.search_client_ssl(val),'wildcard.dev.mask.com-clientssl')

    def test_count_bracket(self):
        val = ['    description "test only"\n', '    destination 10.106.220.50:http\n', '    ip-protocol tcp\n', '    mask 255.255.255.255\n', '    policies {\n', '        asm_auto_l7_policy__virt-svr-sam1 { }\n', '    }\n', '    pool sam-pool-1\n', '    profiles {\n', '        ASM_RHWeb_Base_ASM_Policy { }\n', '        http-x-forwarded-for { }\n', '        tcp { }\n', '        websecurity { }\n', '    }\n', '    security-log-profiles {\n', '        splunk-logging\n', '        splunk-logging_local\n', '    }\n', '    source 0.0.0.0/0\n', '    translate-address enabled\n', '    translate-port enabled\n', '    vlans {\n', '        dev_int_vlan703\n', '    }\n', '    vlans-enabled\n', '    vs-index 3\n']
        self.assertEqual(self.client.count_bracket(val, "{"),9)
        self.assertEqual(self.client.count_bracket(val, "}"),9)

if __name__ == '__main__':
    unittest.main()
