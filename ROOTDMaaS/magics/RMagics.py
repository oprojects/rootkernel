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
CPPRFunctions +='  r.SetVerbose(1);\n'
CPPRFunctions +='  ROOT::R::TRFunctionImport JuPyROOTREvaluate(\".JuPyROOTREvaluate\");\n'
CPPRFunctions +='  TRY {\n'
CPPRFunctions +='     JuPyROOTREvaluate(code);'
CPPRFunctions +='    status=kTRUE;\n'
CPPRFunctions +='  } CATCH(excode) {\n'
CPPRFunctions +='    status=kTRUE;\n'
CPPRFunctions +='  } ENDTRY;\n'
CPPRFunctions +='  return status;\n'
CPPRFunctions +='}\n'


RLoadHandlers = 'Bool_t ROOTDMaaSExecutorRLoadHanlders(TString code)\n'
RLoadHandlers +='{\n'
RLoadHandlers +='  Bool_t status=kFALSE;\n'
RLoadHandlers +='  ROOT::R::TRInterface &r=ROOT::R::TRInterface::Instance();\n'
RLoadHandlers +='  TRY {\n'
RLoadHandlers +='    r.Execute(code);\n'
RLoadHandlers +='    status=kTRUE;\n'
RLoadHandlers +='  } CATCH(excode) {\n'
RLoadHandlers +='    status=kTRUE;\n'
RLoadHandlers +='  } ENDTRY;\n'
RLoadHandlers +='  return status;\n'
RLoadHandlers +='}\n'




RHandlerFunctions="require(evaluate)\n";
RHandlerFunctions+=".JuPyROOTRstdout = function(msg){write(msg, stdout())}\n";
RHandlerFunctions+=".JuPyROOTRstderr = function(msg){write(msg, stderr())}\n";
RHandlerFunctions+=".plot_files = c()\n";
RHandlerFunctions+="assign('.plot_files', c(), envir = .GlobalEnv)\n";
RHandlerFunctions+=".JuPyROOTRPlotHandler = function(obj)\n";
RHandlerFunctions+="{\n";
RHandlerFunctions+="tmpfile=tempfile(tmpdir='.',fileext='.png')\n";
RHandlerFunctions+="png(tmpfile)\n";
RHandlerFunctions+="replayPlot(obj)\n";
RHandlerFunctions+="dev.off()\n";
RHandlerFunctions+=".plot_files = get('.plot_files', envir=.GlobalEnv)\n";
RHandlerFunctions+=".plot_files = append(.plot_files,tmpfile)\n";
RHandlerFunctions+="assign('.plot_files', .plot_files, envir = .GlobalEnv)\n";
RHandlerFunctions+="}\n";
RHandlerFunctions+=".JuPyROOTROutPutHandler  = new_output_handler(text=.JuPyROOTRstdout,error=.JuPyROOTRstderr,graphics=.JuPyROOTRPlotHandler)\n";
RHandlerFunctions+=".JuPyROOTRPrintValues = function(x){\n";
RHandlerFunctions+="classes = evaluate:::classes(x)\n";
RHandlerFunctions+="len = length(x)-1\n";
RHandlerFunctions+="for(i in 1:len){\n";
RHandlerFunctions+="    if(classes[i]=='character') write(x[[i]],stdout())\n";
RHandlerFunctions+="}\n";
RHandlerFunctions+="}\n";
RHandlerFunctions+=".JuPyROOTREvaluate = function(code){\n";
RHandlerFunctions+=".a=evaluate('options(device=pdf)',new_device=0, envir = .GlobalEnv)\n";
RHandlerFunctions+=".b=evaluate(code,output_handler = .JuPyROOTROutPutHandler,envir = .GlobalEnv)\n";
RHandlerFunctions+=".JuPyROOTRPrintValues(.b)\n";
RHandlerFunctions+="}\n";


CPPRPlots = 'std::vector<std::string> ROOTDMaaSExecutorRPlots()\n'
CPPRPlots += '{\n'
CPPRPlots += '  ROOT::R::TRInterface &r=ROOT::R::TRInterface::Instance();\n'
CPPRPlots += '  std::vector<std::string> plots;\n'
CPPRPlots += '  int size;\n'
CPPRPlots += '  r["length(.plot_files)"]>>size;\n'
CPPRPlots += '  if(size>0)r[".plot_files"]>>plots;\n'
CPPRPlots += '  r<<".plot_files = c()";\n'
CPPRPlots += ' return plots;\n'
CPPRPlots += '}\n'



RCompleterCode =  'std::vector<std::string> ROOTDMaaSExecutorRCompleter(TString code)\n'
RCompleterCode += '{\n'
RCompleterCode += '  ROOT::R::TRInterface &r=ROOT::R::TRInterface::Instance();\n'
RCompleterCode += '  r[".line"]<<code;\n'
RCompleterCode += '  r[".cursor_pos"]<<code.Length();  \n'
RCompleterCode += '  r<<"utils:::.assignLinebuffer(.line)";\n'
RCompleterCode += '  r<<"utils:::.assignEnd(.cursor_pos)";\n'
RCompleterCode += '  r<<"utils:::.guessTokenFromLine()";\n'
RCompleterCode += '  r<<"utils:::.completeToken()";\n'
RCompleterCode += '  std::vector<std::string> completions;\n'
RCompleterCode += '  int size;\n'
RCompleterCode += '  r["length(utils:::.retrieveCompletions())"]>>size;\n'
RCompleterCode += '  if(size>0) r["utils:::.retrieveCompletions()"]>>completions;\n'
RCompleterCode += '  r<<"utils:::.guessTokenFromLine(update = FALSE)";\n'
RCompleterCode += '  return completions;\n'
RCompleterCode += '}\n'


RExecutor = None
RExecutorPlots = None
RCompleter = None

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

def RExecutorLoadHandlers(kernel):
    status = kernel.Declarer(str(RLoadHandlers))
    if status:
        try:
            from ROOT import ROOTDMaaSExecutorRLoadHanlders
            ROOTDMaaSExecutorRLoadHanlders(str(RHandlerFunctions))
        except ImportError:
            raise Exception("Error: importing ROOTDMaaSExecutorRLoadHanlders)")

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

def LoadRCompleter(kernel):
    global RCompleter
    status = False
    if not RCompleter:
        status = kernel.Declarer(str(RCompleterCode))
        if status:
            try:
                from ROOT import ROOTDMaaSExecutorRCompleter
                RCompleter = ROOTDMaaSExecutorRCompleter
            except ImportError:
                raise Exception("Error: importing ROOTDMaaSExecutorRCompleter)")


#NOTE:actually ROOTaaS is not capturing the error on %%cpp -d if the function is wrong 
class RMagics(Magic):
    def __init__(self, kernel):
        super(RMagics, self).__init__(kernel)
        global RExecutor
        global RExecutorPlots
        global RCompleter
        self.RExecutor = RExecutor
        self.RExecutorPlots = RExecutorPlots
        self.RCompleter = RCompleter

    def cell_r(self, args):
        '''Executes the content of the cell as R code.'''                
        if self.code.strip():
             self.kernel.ioHandler.clear()
             self.kernel.ioHandler.InitCapture()
             self.RExecutor(str(self.code))
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
        self.evaluate = False
    def get_completions(self, info):
        if self.RCompleter is not None:
            return self.RCompleter(str(info['code']))
        else:
            return []
        
def register_magics(kernel):
    #trying to load ROOT-R stuff
    #if ROOT-R is not installed then the magics will not be loaded
    kernel.Executor('#include<TRInterface.h>')
    RExecutorLoadHandlers(kernel)
    LoadRExecutor(kernel)
    LoadRExecutorPlots(kernel)
    LoadRCompleter(kernel)
    global RExecutor
    if RExecutor is not None:
        kernel.register_magics(RMagics)
    
