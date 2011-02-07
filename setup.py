#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://www.tlvince.com/contact/>

"""The distutils script to build and install timed."""

from distutils.core import setup

setup(
    name  =  'timed',
    version = '0.1.1',
    scripts = ['timed.py'],
    description = "command-line time tracking",
    long_description = open('README.mkd').read(),
    url = 'http://tlvince.github.com/timed',
    author = 'Tom Vincent',
    author_email = 'http://www.tlvince.com/contact/',
    license = 'BSD',
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Topic :: Utilities',
    ]
)
