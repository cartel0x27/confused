#! /usr/bin/env python
try:
  from setuptools import setup, Extension
except ImportError:
  from distutils.core import setup, Extension

import sys
import os 

long_description = """\
PAM module that implements Confused on unix."""

classifiers = [
  "Development Status :: 4 - Beta",
  "Intended Audience :: Developers",
  "License :: OSI Approved :: WTFPL",
  "Natural Language :: English",
  "Operating System :: Unix",
  "Programming Language :: C",
  "Programming Language :: Python",
  "Topic :: System :: Systems Administration :: Authentication/Directory"]

if not os.environ.has_key("Py_DEBUG"):
  Py_DEBUG = []
else:
  Py_DEBUG = [('Py_DEBUG',1)]

setup(
  name="confused",
  version="0.2.0",
  description="Confused for Linux",
  keywords="pam,embed,authentication,security,deniable",
  platforms="Unix",
  long_description=long_description,
  author="Cartel",
  author_email="cartel@thoughtcrime.org.nz",
  url="http://this.is.thoughtcrime.org.nz/confused",
  license="WTFPL",
  classifiers=classifiers,
  py_modules = ["confused"]
  )
