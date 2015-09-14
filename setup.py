#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup
import src.icd as icd

PACKAGE = "icd-10"
NAME = "ICD-ten"
DESCRIPTION = "pygtk application for find ICD-10 codes"
AUTHOR = "aweal"
AUTHOR_EMAIL = "gaweal@gmail.com"
URL = "github.com/aweal/icd-10"

VERSION = icd.__version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read("README.md"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    packages=['icdten'],
    package_dir={'translate': 'src/icd'},

    data_files=[
        ("share/icons/hicolor/scalable/apps", ['resources/icd-ten.svg']),
        ("share/icons/hicolor/48x48/apps", ['resources/icd-ten.svg']),
        ("share/applications", ['resources/ICD-ten.desktop'])
    ],

    entry_points={'gui_scripts': [
        'icd-ten = icd.application:run',
    ]},

    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: X11 Applications :: GTK",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    zip_safe=False, requires=['gi', 'pysqlite'],
    test_suite="tests"
)
