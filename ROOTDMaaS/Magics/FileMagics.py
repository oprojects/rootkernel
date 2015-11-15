from ROOTaaS.iPyROOT import utils 
from metakernel import Magic, option
from metakernel.display import clear_output, display, HTML


class DocMagics(Magic):
    def __init__(self, kernel):
        super(DocMagics, self).__init__(kernel)
    
    @option(
        '-r', '--root', action='store', help='Display gui to show ROOT file'
    )            
    def cell_file(self,*args,**kwargs):
        '''Executes JSROOT Guy to see ROOT files'''
        if kwargs["root"]:
           htmlcode = "<script type='text/javascript' src='https://root.cern.ch/js/dev/scripts/JSRootCore.js?gui'></script>"
           #htmlcode += "<div id='simpleGUI' files='"+kwargs["root"]+"' path=''>loading files ... </div>"
           htmlcode += "<iframe width='100%' height='500px'src='https://root.cern.ch/js/dev/?file="+kwargs["root"]+"&autoload="+kwargs["root"]+"' ></iframe>"
           display(HTML(htmlcode))
        self.evaluate = False
        
    @option(
        '-r', '--root', action='store', help='Display gui to show ROOT file'
    )            
    def line_file(self, *args,**kwargs):
        '''Executes JSROOT Guy to see ROOT files'''
        self.cell_help(args,kwargs)
        
def register_magics(kernel):
    kernel.register_magics(DocMagics)