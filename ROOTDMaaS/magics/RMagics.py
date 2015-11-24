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

import IPython.display

import sys
import os
#C Function to Execute R code
CPPRFunctions ='Bool_t ROOTDMaaSExecutorR(TString code)\n'
CPPRFunctions +='{\n'
CPPRFunctions +='  Bool_t status=kFALSE;\n'
CPPRFunctions +='  ROOT::R::TRInterface &r=ROOT::R::TRInterface::Instance();\n'
CPPRFunctions +='  TRY {\n'
CPPRFunctions +='    r.Execute(code);\n'
CPPRFunctions +='    status=kTRUE;\n'
CPPRFunctions +='  } CATCH(excode) {\n'
CPPRFunctions +='    status=kTRUE;\n'
CPPRFunctions +='  } ENDTRY;\n'
CPPRFunctions +='  return status;\n'
CPPRFunctions +='}\n'

CPPRPlots = 'std::vector<std::string> ROOTDMaaSExecutorRPlots()\n'
CPPRPlots += '{\n'
CPPRPlots += '  ROOT::R::TRInterface &r=ROOT::R::TRInterface::Instance();\n'
CPPRPlots += '  std::vector<std::string> plots;\n'
CPPRPlots += '  r[".files"]>>plots;\n'
CPPRPlots += ' return plots;\n'
CPPRPlots += '}\n'



#R Functions to capture plots
RPlotFunctions =  'options(device="png")\n'
RPlotFunctions += '.files = c()\n'
RPlotFunctions += '.dev.new = dev.new\n'
RPlotFunctions += '.png = png\n'
RPlotFunctions += 'assign(".files", c(), envir = .GlobalEnv)\n'
RPlotFunctions += 'assign(".dev.new",dev.new, envir = .GlobalEnv)\n'
RPlotFunctions += 'assign(".png",png, envir = .GlobalEnv)\n'
RPlotFunctions += 'png = function(filename = "Rplot.png",\n'
RPlotFunctions += '         width = 800, height = 600, units = "px", pointsize = 15,\n'
RPlotFunctions += '          bg = "white",  res = NA, ...,\n'
RPlotFunctions += '          type = c("cairo", "cairo-png", "Xlib", "quartz"), antialias)\n'
RPlotFunctions += '{\n'
RPlotFunctions += '.png = get(".png", envir=.GlobalEnv)\n'
RPlotFunctions += 'tmpfile=filename\n'
RPlotFunctions += 'if(filename == "Rplot.png")\n'
RPlotFunctions += '{\n'
RPlotFunctions += '  tmpfile=tempfile(tmpdir=".",fileext=".png")\n'
RPlotFunctions += '}\n'
RPlotFunctions += '.png(tmpfile,width,height,units,pointsize,bg,res)\n'
RPlotFunctions += '.files = get(".files", envir=.GlobalEnv)\n'
RPlotFunctions += '.files = append(.files,tmpfile)\n'
RPlotFunctions += 'assign(".files", .files, envir = .GlobalEnv)\n'
RPlotFunctions += '}\n'

RPlotFlush = 'for (i in dev.list())\n'
RPlotFlush += '{\n'
RPlotFlush += 'dev.set(i)\n'
RPlotFlush += 'dev.flush()\n'
RPlotFlush += 'dev.off()\n'
RPlotFlush += '}\n'



RExecutor = None
RExecutorPlots = None

#needs error control if ROOT-R is not installed
def LoadRExecutor(kernel):
    global RExecutor
    status = False
    if not RExecutor:
        status = kernel.Declarer(str(CPPRFunctions))
        if status:
            try:
                from ROOT import ROOTDMaaSExecutorR
                RExecutor = ROOTDMaaSExecutorR
            except ImportError:
                raise Exception("Error: importing ROOTDMaaSExecutorR)")

def LoadRExecutorPlots(kernel):
    global RExecutorPlots
    status = False
    if not RExecutorPlots:
        status = kernel.Declarer(str(CPPRPlots))
        if status:
            try:
                from ROOT import ROOTDMaaSExecutorRPlots
                RExecutorPlots = ROOTDMaaSExecutorRPlots
            except ImportError:
                raise Exception("Error: importing ROOTDMaaSExecutorRPlots)")


#NOTE:actually ROOTaaS is not capturing the error on %%cpp -d if the function is wrong 
class RMagics(Magic):
    def __init__(self, kernel):
        super(RMagics, self).__init__(kernel)
        global RExecutor
        global RExecutorPlots
        self.RExecutor = RExecutor
        self.RExecutorPlots = RExecutorPlots
        self.RExecutor("options(device='png')")

    def cell_r(self, args):
        '''Executes the content of the cell as R code.'''                
        if self.code.strip():
             self.kernel.ioHandler.clear()
             self.kernel.ioHandler.InitCapture()
             self.RExecutor(str(self.code))
             self.RExecutor(str(RPlotFlush))
             self.kernel.ioHandler.EndCapture()
             std_out = self.kernel.ioHandler.getStdout()
             std_err = self.kernel.ioHandler.getStderr()
             if std_out != "":
                stream_content_stdout = {'name': 'stdout', 'text': std_out}
                self.kernel.send_response(self.kernel.iopub_socket, 'stream', stream_content_stdout)
             if std_err != "":
                stream_content_stderr = {'name': 'stderr', 'text': std_err}
                self.kernel.send_response(self.kernel.iopub_socket, 'stream', stream_content_stderr)
             if self.RExecutorPlots:
                 plots=RExecutorPlots()
                 for i in plots:
                    img = IPython.display.Image(filename=i, format='png', embed=True)
                    self.kernel.Display(img)
                    os.unlink(i)
             self.RExecutor('.files = c()')
        self.evaluate = False
        
def register_magics(kernel):
    #trying to load ROOT-R stuff
    #if ROOT-R is not installed then the magics will not be loaded
    kernel.Executor('#include<TRInterface.h>')
    LoadRExecutor(kernel)
    LoadRExecutorPlots(kernel)
    global RExecutor
    if RExecutor is not None:
        RExecutor(RPlotFunctions)
        kernel.register_magics(RMagics)
    