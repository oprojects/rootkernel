from ROOTaaS.iPyROOT import utils 
from metakernel import Magic, option
from metakernel.display import clear_output, display, HTML

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
           display(HTML(htmlcode))
        else:
           docurl='http://rootdoc.oproject.org/rootdoc/html/class'+kwargs["class"].replace(':','_1')+'.html'
           htmlcode="<iframe src='"+docurl+"' width='100%' height='400px' ></iframe>"
           display(HTML(htmlcode))
        self.evaluate = False
        
    @option(
        '-c', '--class', action='store', help='Display help of given class'
    )            
    @option(
        '-n', '--namespace', action='store', help='Display help of given namespace'
    )            
    def line_doc(self, *args,**kwargs):
        '''Executes the content of the cell as C++ code.'''
        self.cell_help(args,kwargs)
        
def register_magics(kernel):
    kernel.register_magics(DocMagics)