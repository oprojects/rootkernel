import ROOT
import sys, os, select
from ROOTaaS.iPyROOT.utils import StreamCapture as InternalStreamCapture
from ROOTaaS.iPyROOT.utils import CanvasDrawer as InternalCanvasDrawer

from ROOTaaS.iPyROOT.utils import _jsCanvasWidth, _jsCanvasHeight, _jsROOTSourceDir, _jsCode


class StreamCapture(InternalStreamCapture):
    def __init__(self,stream):
        InternalStreamCapture.__init__(self,stream)
        
    def post_execute(self):
        out = ''
        if self.pipe_out:
            while self.more_data():
                out += os.read(self.pipe_out, 1024)

        self.flush()
        self.sysStreamFile.write(out) # important to print the value printing output
        return out
      
class CanvasDrawer(InternalCanvasDrawer):
    def __init__(self, thePad):
        InternalCanvasDrawer.__init__(self,thePad)
        
    def jsCode(self):
        # Workaround to have ConvertToJSON work
        pad = ROOT.gROOT.GetListOfCanvases().FindObject(ROOT.gPad.GetName())
        json = ROOT.TBufferJSON.ConvertToJSON(pad, 3)
        #print "JSON:",json

        # Here we could optimise the string manipulation
        divId = 'root_plot_' + str(self._getUID())
        thisJsCode = _jsCode.format(jsCanvasWidth = _jsCanvasWidth,
                                    jsCanvasHeight = _jsCanvasHeight,
                                    jsROOTSourceDir = _jsROOTSourceDir,
                                    jsonContent=json.Data(),
                                    jsDrawOptions="",
                                    jsDivId = divId)

        return thisJsCode 
  