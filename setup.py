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

import setuptools


setuptools.setup(
    name="slugs",
    version="1.0.0",
    description="A Simple, Lightweight User Group Service.",
    keywords="authentication",
    author="Peter Hamilton",
    author_email="peter.allen.hamilton@gmail.com",
    url="",
    license="Apache License, Version 2.0",
    entry_points={
        'console_scripts': [
            'slugs = slugs.app:main'
        ]
    },
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
