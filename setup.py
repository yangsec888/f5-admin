from setuptools import setup
from setuptools import find_packages
import re
import os

def get_property(prop):
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    ini_file = cur_dir + "/__init__.py"
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(ini_file).read())
    return result.group(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="f5_admin",
    version=get_property("__version__"),
    author="Sam Li",
    author_email="yangsec888@gmail.com",
    description="Simple python package to manipulate F5 running configuration better and faster",
    long_description_content_type='text/markdown',
    long_description=long_description,
    keywords = "DIY F5 Admin API / Utilities",
    #long_description_content_type="text/markdown",
    url="https://github.com/yangsec888/f5-admin",
    packages=['f5_admin', ],
    package_dir={'f5_admin': 'src'},
    include_package_data=True,
    scripts=['src/bin/f5-get', 'src/bin/f5-put', 'src/bin/f5-run', 'src/bin/f5-runs', 'src/bin/f5-sync',
            'src/bin/f5-backup', 'src/bin/f5-standby', 'src/bin/f5-resolve',
            'src/bin/f5-search', 'src/bin/f5-fetch','src/bin/f5-install-cert', 'src/bin/f5-delete',
            'src/bin/asm-get', 'src/bin/asm-put', 'src/bin/asm-fetch',
            'src/bin/dg-get', 'src/bin/dg-put',
            'src/bin/oom-mon'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
    ],
    install_requires=[
        'paramiko>=2.4.1',
        'beautifulsoup4',
        'xmltodict'
    ]
)
