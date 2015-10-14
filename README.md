# ROOT Kernel

ROOT Kernel for Jupyter.

## Limitations
* It dont support declare functions in cell, but classes is supported if methods are declare inside
* The plots are only in png, JSROOT will be implemented soon
* The plot just work if the method Draw is called by TCanvas's object

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
