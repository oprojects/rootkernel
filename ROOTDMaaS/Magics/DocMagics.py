from ROOTaaS.iPyROOT import utils 
from metakernel import Magic, option
from metakernel.display import clear_output, display, HTML

import urllib2

class DocMagics(Magic):
    def __init__(self, kernel):
        super(DocMagics, self).__init__(kernel)
    
    @option(
        '-c', '--class', action='store', default="default", help='Display documentation of given class'
    )            
    @option(
        '-n', '--namespace', action='store', default="default", help='Display documentation of given namespace'
    )            
    def cell_doc(self, *args):
        '''Executes the search of documentation for classes'''
        print(args)
        docurl='http://rootdoc.oproject.org/rootdoc/html/class'+args.replace(':','_1')+'.html'
        htmlcode="<iframe src='"+docurl+"' width='100%' height='400px' ></iframe>"
        display(HTML(htmlcode))

        #try:
           #urllib2.urlopen(docurl)
        #except urllib2.HTTPError, e:
           #print("http"+e.code)
        #except urllib2.URLError, e:
           #print("url"+e.args)        
        
    @option(
        '-c', '--class', action='store', default="default", help='Display help of given class'
    )            
    @option(
        '-n', '--namespace', action='store', default="default", help='Display help of given namespace'
    )            
    def line_doc(self, *args):
        '''Executes the content of the cell as C++ code.'''
        self.cell_help(args)
        
def register_magics(kernel):
    kernel.register_magics(DocMagics)