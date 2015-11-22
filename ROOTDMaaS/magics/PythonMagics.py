import ROOT
from ROOTDMaaS.js.JSROOT import CanvasDrawer

from metakernel.display import HTML
from metakernel.magics.python_magic import  PythonMagic

class PythonMagics(PythonMagic):
    def __init__(self, kernel):
        super(PythonMagics, self).__init__(kernel)
        self.post_process = self._post_process
    def _post_process(self, retval):
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
        if retval is not None:
            return retval
        else:
            return self.retval
        
def register_magics(kernel):
    kernel.register_magics(PythonMagics)