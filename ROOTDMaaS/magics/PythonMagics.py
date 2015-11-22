import ROOT
from ROOT import TPython
from ROOTDMaaS.js.JSROOT import CanvasDrawer

from metakernel.display import HTML
from metakernel import Magic, option

class PythonMagics(Magic):
    def __init__(self, kernel):
        super(PythonMagics, self).__init__(kernel)
                
    def cell_python(self,args):
        '''Executes the content of the cell as python code.'''
        if self.code.strip():
            self.kernel.ioHandler.clear()
            self.kernel.ioHandler.InitCapture()
            TPython.Exec(str(self.code))
            self.kernel.ioHandler.EndCapture()
            std_out = self.kernel.ioHandler.getStdout()
            std_err = self.kernel.ioHandler.getStderr()
            stream_content_stdout = {'name': 'stdout', 'text': std_out}
            self.kernel.send_response(self.kernel.iopub_socket, 'stream', stream_content_stdout)
            if std_err != "":
                stream_content_stderr = {'name': 'stderr', 'text': std_err}
                self.kernel.send_response(self.kernel.iopub_socket, 'stream', stream_content_stderr)
            canvaslist = ROOT.gROOT.GetListOfCanvases()
            if canvaslist:
                for canvas in canvaslist:
                    if canvas.IsDrawn():
                        self.drawer = CanvasDrawer(canvas)
                        if self.drawer._canJsDisplay():
                            self.kernel.Display(HTML(self.drawer._jsDisplay()))
                        else:
                            self.kernel.Display(self.drawer._pngDisplay())
                        canvas.ResetDrawn()
        #self.code = ''
        self.evaluate = False
#NOTE:python tab completions is not working into the cell
    #def get_completions(self, info):
        #python_magic = self.kernel.line_magics['python']
        #return python_magic.get_completions(info)        

def register_magics(kernel):
    kernel.register_magics(PythonMagics)