# ROOT Kernel

ROOT Kernel for Jupyter.

## Limitations
* It dont support declare functions in cell, but classes is supported
* The plots are only in png, JSROOT will be implemented soon
* The plot just work if the method Draw is called by TCanvas's object

## Install

Prerequsites
    pip install metakernel

To install the kernel:

    jupyter kernelspec install root

or for IPython/Jupyter < 4:

    ipython kernelspec install root
