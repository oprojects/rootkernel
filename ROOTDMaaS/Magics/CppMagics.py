from ROOTaaS.iPyROOT import utils 
from metakernel import Magic, option

class CppMagics(Magic):
    def __init__(self, kernel):
        super(CppMagics, self).__init__(kernel)
                
    @option(
        '-a', '--aclic', action='store', default="default", help='Compile code with ACLiC.'
    )
    @option(
        '-d', '--declare', action='store', default=None, help='Declare functions and/or classes.'
    )
    def cell_cpp(self, args):
        '''Executes the content of the cell as C++ code.'''
        if self.code.strip():
             if args=='-a':
                 utils.invokeAclic(self.code)
             elif args=='-d':
                 utils.declareCppCode(self.code)
             else:
                 utils.processCppCode(self.code)
        #self.code = ''
        self.evaluate = False
        
    @option(
        '-a', '--aclic', action='store', default="default", help='Compile code with ACLiC.'
    )
    @option(
        '-d', '--declare', action='store', default=None, help='Declare functions and/or classes.'
    )
    def line_cpp(self, args):
        '''Executes the content of the cell as C++ code.'''
        self.cell_cpp(args)

def register_magics(kernel):
    kernel.register_magics(CppMagics)