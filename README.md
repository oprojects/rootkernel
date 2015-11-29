# ROOT Kernel

ROOT(C++) Jupyter Kernel for the project  ROOTDMaaS (ROOT Data Mining as a Service)

## Features
* C++  highlighting
* C++ Tab-completion
* Python(Magic Cell)  highlighting
* Python(Magic Cell) Tab-completion (using jedi)
* R(Magic Cell)  highlighting
* R(Magic Cell) Tab-completion (using jedi)
* JSROOT implemented
* ipython magics supported(shell,python,html,etc..)
* I/O capture for segfault and in general
* new magic added %%doc to show documentation for classes
* magics %%cpp to declare functions and classes in cells or to compile with ACLiC
* Tested under Gnu/Linux and MacOSX Yisemite

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
Authors: 
* Omar Zapata <Omar.Zapata@cern.ch> OProject
* Danilo Piparo <Danilo.Piparo@cern.ch> CERN
* Enric Tejedor <enric.tejedor.saavedra@cern.ch> CERN

website: http://oproject.org/ROOT+Jupyter+Kernel (information only for ROOT kernel)

Distributed under the terms of the Modified LGPLv3 License.

