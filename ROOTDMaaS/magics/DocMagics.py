# -*- coding:utf-8 -*-
#-----------------------------------------------------------------------------
#  Copyright (c) 2015, ROOT Team.
#  Authors: Omar Zapata <Omar.Zapata@cern.ch> http://oproject.org
#  website: http://oproject.org/ROOT+Jupyter+Kernel (information only for ROOT kernel)
#  Distributed under the terms of the Modified BSD License.
#
#  The full license is in the file COPYING.rst, distributed with this software.
#-----------------------------------------------------------------------------
from metakernel import Magic, option
from metakernel.display import HTML

import urllib2, re

class DocMagics(Magic):
    def __init__(self, kernel):
        super(DocMagics, self).__init__(kernel)
    
    @option(
        '-c', '--class', action='store', help='Display documentation of given class'
    )            
    @option(
        '-n', '--namespace', action='store', help='Display documentation of given namespace'
    )            
    def cell_doc(self,*args,**kwargs):
        '''Executes the search of documentation for classes'''
        if kwargs["namespace"]:
           docurl='http://rootdoc.oproject.org/rootdoc/html/namespace'+kwargs["namespace"].replace(':','_1')+'.html'
           htmlcode="<iframe src='"+docurl+"' width='100%' height='400px' ></iframe>"
           self.kernel.Display(HTML(htmlcode))
        else:
           docurl='http://rootdoc.oproject.org/rootdoc/html/class'+kwargs["class"].replace(':','_1')+'.html'
           htmlcode="<iframe src='"+docurl+"' width='100%' height='400px' ></iframe>"
           self.kernel.Display(HTML(htmlcode))
        self.evaluate = False
        
        
def register_magics(kernel):
    kernel.register_magics(DocMagics)