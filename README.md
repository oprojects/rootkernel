# ROOT Kernel

ROOT(C++) Kernel for Jupyter using the ROOTDMaaS (ROOT Data Mining as a Service)

## Features
* C++  highlighting
* Tab-completion
* JSROOT implemented
* ipython magics supported(shell,python,html,etc..)
* I/O capture for segfault and in general
* new added %%doc to show documentation for classes
* magics %%cpp to declare functions and classes in cells or tu compile with ACLiC


## Limitations
* It dont support declare functions and classes without magic %%cpp
* The plot just work if the method Draw is called by TCanvas's object
* The output stdout/stderr just can buffer 1Mb(PIPE buffer) 


## Install

Prerequsites

    pip install metakernel
    pip install jedi
    git clone https://github.com/oprojects/rootkernel.git
    cd rootkernel.git
    
    python setup.py build
    python setup.py install
    ipython kernelspec install root
    
    or
    
    make

To install the kernel:

    jupyter kernelspec install root

or for IPython/Jupyter < 4:

    ipython kernelspec install root

##  Copyright (c) 2015, ROOT Team.
  Authors: Omar Zapata <Omar.Zapata@cern.ch> oproject.org
           Danilo Piparo <Danilo.Piparo@cern.ch> CERN
           Enric Tejedor enric.tejedor.saavedra@cern.ch> CERN
  website: http://oproject.org/ROOT+Jupyter+Kernel (information only for ROOT kernel)
  Distributed under the terms of the Modified BSD License.

