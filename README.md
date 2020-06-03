[![image](/images/f5_logo.png)](https://github.com/yangsec888/f5-admin)
================================================================================

- [What is it?](#what-is-it)
  - [Release Notes](#release-notes)
- [How Does It Work?](#how-does-it-work)
  - [Running Requirement?](#running-requirement)
  - [Working Examples?](#working-examples)
  - [API Documents](#api-documents)
  - [Unit Testing](#unit-testing)
- [Installation](#installs)
  - [Install from Python Package Repository](#install-from-python-package-repository)
  - [Build from Source](#build-the-python-package-from-source)
  - [Install from Build Package](#install-from-build-package)
  - [Verify the Installation](#verify-the-installation)
- [To Do](#to-do)
- [Who is this guy](#who-is-this-guy)
  - [License](LICENSE.txt)

---

## What is it?
I call it DIY F5 Security Administrators's Swiss Army knife. This is a simple python API built for F5 security administrators.

I implemented the Python package in order to better understand and help manage my employer F5 infrastructure. Which has a whopping 32 nodes in total, and over half million running configuration lines when combined together as of this writing.

### Release Notes
Check out [Releases](Releases.md) document for complete information.

---

## How Does It Work?
The package provides a direct hook to the <a href="https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/tmos-concepts-11-2-0.html" target="_blank">F5 TMOS</a> command line interface from your local workstation, by establishing a TTY connection via SSH as the privileged user. Once hooked, the security admin will be able to
manipulate F5 running configuration by using the standard TMOS commands.

Furthermore, the security admin can go to the next level of the playing field, by custom buildout the  automation procedures in the full-stack capable, object-oriented Python programming language from there.

### Running Requirement?
As of November 11 2019, you'll need Python 3 environment to run the package.

The package is originally developed in Python 2.7 environment of my Macbooks Pro. Since Python 2 is depreciated end of 2019, the package is converted into [Python 3](https://www.python.org/downloads/) from version 1.1.16 onward. Note I have no plan to backward supporting 2.7.

Checking your Python version with the command below:
```bash
$ python -V
```

### Working Examples?
Please refer to the [utility examples](/START.md) documents for the working examples.

### API Documents
Please refer to [API](/API.md), for complete information on how to use this API.

### Unit Testing ###
[Unit tests](/tests) are written to ensure the quality of the code. It provides the assurance and sustainability of the project. Use the following command to run the tests:

```bash
$ cd f5-admin/
$ python -m unittest discover tests/
```

---

## Installations
There are several ways you can install the Python package in your favorite system.

### Install from Python Package Repository
```bash
$ pip install f5-admin
```

### Build the Python Package from Source
Once you [download and unzip](https://github.com/yangsec888/f5-admin/repository/master/archive.zip) the source code, find and run the rebuild.sh script under the source root directory:

```bash
$ python setup.py sdist bdist_wheel
```

### Install from Build Package
After the successful build, you'll also have the .gz package under 'dist' sub-folder.  You have the option to distribute it to other systems. And you can then install the software by using the Python standard package management tool [pip](https://pypi.org/project/pip/).

For example:
```bash
$ sudo pip install dist/f5_admin-1.1.2.tar.gz
Password:
...
Successfully installed f5-admin-1.1.2
```

### Verify the Installation
Once installed, you'll be able to list it under your Python environment:
```bash
$ pip list | grep f5
f5-admin                               1.2.0
```

---

## To Do
Refer to [TODO](/TODO.md) document for complete list of expectations / project roadmap.
## Who is this guy?
Sam (Yang) Li serves as the IT Security Architect in the infrastructure team. He is an information security veteran with 20 years hand-on experiences in the fields. You can connect him in [LinkedIn](https://www.linkedin.com/in/yangli8/).
### [License](/LICENSE.txt)
