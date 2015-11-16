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
* It dont support declare functions in cell, but classes is supported if methods are declare inside
* The plot just work if the method Draw is called by TCanvas's object
* It dont c++ tracebacks 
* Magics not implemented yet.

## Install

Prerequsites

    pip install metakernel
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
