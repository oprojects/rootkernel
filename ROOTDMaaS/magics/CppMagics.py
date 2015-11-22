from ROOTaaS.iPyROOT import utils 
from metakernel import Magic, option

import sys

from rootkernelutils import GetIOHandler, GetExecutor,GetDeclarer 

#NOTE:actually ROOTaaS is not capturing the error on %%cpp -d if the function is wrong 
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
             self.kernel.ioHandler.clear()
             self.kernel.ioHandler.InitCapture()
             
             if args=='-a':
                 utils.invokeAclic(self.code)
             elif args=='-d':
                 self.kernel.Declarer(str(self.code))
             else:
                 self.kernel.Executor(str(self.code))
             self.kernel.ioHandler.EndCapture()
             std_out = self.kernel.ioHandler.getStdout()
             std_err = self.kernel.ioHandler.getStderr()
             if std_out != "":
                stream_content_stdout = {'name': 'stdout', 'text': std_out}
                self.kernel.send_response(self.kernel.iopub_socket, 'stream', stream_content_stdout)
             if std_err != "":
                stream_content_stderr = {'name': 'stderr', 'text': std_err}
                self.kernel.send_response(self.kernel.iopub_socket, 'stream', stream_content_stderr)
            
        self.evaluate = False
        
def register_magics(kernel):
    kernel.register_magics(CppMagics)