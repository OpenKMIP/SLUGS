#!/usr/bin/env python
#
# Copyright 2017, The Johns Hopkins University/Applied Physics Laboratory
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
import re
import setuptools

# Dynamically set __version__
version_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'slugs',
    'version.py'
)
with open(version_path, 'r') as version_file:
    mo = re.search(
        r"^.*= '(\d\.\d\..*)'$",
        version_file.read(),
        re.MULTILINE
    )
    __version__ = mo.group(1)


setuptools.setup(
    name="slugs",
    version=__version__,
    description="A Simple, Lightweight User Group Service.",
    keywords="authentication",
    author="Peter Hamilton",
    author_email="peter.allen.hamilton@gmail.com",
    url="https://github.com/OpenKMIP/SLUGS",
    license="Apache License, Version 2.0",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'slugs = slugs.app:main'
        ]
    },
    install_requires=[
        "cherrypy>=13.0.0"
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: CherryPy",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ]
)
