#!/usr/bin/env python
# -*- coding:utf-8 -*-
#-----------------------------------------------------------------------------
#  Copyright (c) 2015, ROOT Team.
#  Authors: Omar Zapata <Omar.Zapata@cern.ch> http://oproject.org
#           Danilo Piparo <Danilo.Piparo@cern.ch> CERN
#           Enric Tejedor enric.tejedor.saavedra@cern.ch> CERN
#  website: http://oproject.org/JuPyROOT (information only for ROOT kernel)
#  Distributed under the terms of the Modified LGPLv3 License.
#
#  The full license is in the file COPYING.rst, distributed with this software.
#-----------------------------------------------------------------------------

from __future__ import print_function

# the name of the project
name = 'JuPyROOT'

#-----------------------------------------------------------------------------
# Minimal Python version sanity check
#-----------------------------------------------------------------------------

import sys

v = sys.version_info
if v[:2] < (2,7) or (v[0] >= 3 and v[:2] < (3,3)):
    error = "ERROR: %s requires Python version 2.7 or 3.3 or above." % name
    print(error, file=sys.stderr)
    sys.exit(1)

PY3 = (sys.version_info[0] >= 3)

#-----------------------------------------------------------------------------
# get on with it
#-----------------------------------------------------------------------------

import os
from glob import glob

from distutils.core import setup

pjoin = os.path.join
here = os.path.abspath(os.path.dirname(__file__))
pkg_root = pjoin(here, name)

MAGICSPATH = "JuPyROOT/magics/"

##reading ROOT modules and Magics
root_modules =  ['ROOTKernel','JuPyROOT/io/Handler','JuPyROOT/js/JSROOT']
root_modules += ['JuPyROOT/kernel/CppCompleter','JuPyROOT/kernel/Utils']
root_modules += ['JuPyROOT/__init__','JuPyROOT/io/__init__','JuPyROOT/js/__init__','JuPyROOT/kernel/__init__']
os.chdir(MAGICSPATH)
for file in glob("*.py"):
    root_modules.append(MAGICSPATH+file.replace(".py",""))
os.chdir("../..")
#print(root_modules)
    
setup_args = dict(
    name            = name,
    version         = '0.0.1',
    py_modules      = root_modules,
    scripts         = glob(pjoin('scripts', '*')),
    description     = "CERN's ROOT/C++ Kernel for Jupyter",
    author          = 'Omar Zapata, Danilo Piparo, Enric Tejedor',
    author_email    = 'Omar.Zapata@cern.ch',
    url             = 'http://oproject.org/ROOT%20Jupyter%20Kernel',
    license         = 'LGPLv3',
    platforms       = "Linux, Mac OS X",
    keywords        = ['Interactive', 'Interpreter', 'Shell', 'Web','ROOT'],
    classifiers     = [
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: LGPLv3 License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)

if 'develop' in sys.argv or any(a.startswith('bdist') for a in sys.argv):
    import setuptools

setuptools_args = {}
install_requires = setuptools_args['install_requires'] = [
    'ipython',
    'pyzmq',
    'tornado',
    'pexpect',
    'jedi',
    'metakernel',
    'jupyter'
]

if 'setuptools' in sys.modules:
    setup_args.update(setuptools_args)

if __name__ == '__main__':
    setup(**setup_args)

