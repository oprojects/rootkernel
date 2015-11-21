#!/usr/bin/env python

from __future__ import print_function

import sys, os, select, tempfile


#trying to find ROOT lib path to PYTHONPATH 
#NOTE: required for hupyterhub              
try:
    ROOT_PYTHON_PATH = os.popen("root-config --libdir")
    os.environ['PYTHONPATH'] = os.environ['PYTHONPATH']+":"+ROOT_PYTHON_PATH.read()
    ROOT_PYTHON_PATH.close()
except Exception as e:
    pass

#ROOT related imports
try:
    import ROOT
except ImportError:
    raise Exception("Error: PyROOT not found")


try:
    from ROOTaaS.iPyROOT import utils 
    from ROOTaaS.iPyROOT.cppcompleter import CppCompleter
except ImportError:
    raise Exception("Error: ROOTaaS not found")

import IPython

try:
    from metakernel import MetaKernel, Parser
    from metakernel.display import clear_output, display, HTML
except ImportError:
    raise Exception("Error: package metakernel not found.(install it running 'pip install metakernel')")

from rootkernelutils import GetIOHandler, GetExecutor,GetDeclarer, CanvasDrawer
from rootkernelmagics import MagicLoader
     
# We want iPython to take over the graphics
ROOT.gROOT.SetBatch()

_debug = True

def Debug(msg):
     print('out: %r' % msg, file=sys.__stderr__)
        

class ROOTKernel(MetaKernel):
    implementation = 'ROOT'
    implementation_version = '1.0'
    language = 'c++'
    language_version = '0.1'
    language_info = {'name': 'c++',
                     'codemirror_mode': 'text/x-c++src',
                     'mimetype': ' text/x-c++src',
                     'file_extension': '.C'}
    banner = "CERN's ROOT Kernel(ROOTaaS)"
    def __init__(self,**kwargs):
        
        MetaKernel.__init__(self,**kwargs)
        utils.enableJSVis()
        utils.enableJSVisDebug()
        utils.setStyle()
        utils.enhanceROOTModule()
        self.magicloader=MagicLoader(self)
        
        self.ioHandler = GetIOHandler()
        self.Executor  = GetExecutor()
        self.Declarer  = GetDeclarer()#required for %%cpp -d magic
        self.parser = Parser(self.identifier_regex, self.func_call_regex,
                             self.magic_prefixes, self.help_suffix)
        self.completer = CppCompleter()
        self.completer.activate()

    def get_completions(self, info):
        if _debug :Debug(info)
        return self.completer._completeImpl(info['code'])
    
    #def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):      
    def do_execute_direct(self, code, silent=False):
        
        if not code.strip():
            return

        status = 'ok'
        traceback = None
        std_out=""
        std_err=""
        try:
            self.ioHandler.clear()
            self.ioHandler.InitCapture()
            root_status = self.Executor(str(code))
            self.ioHandler.EndCapture()
            
            std_out = self.ioHandler.getStdout()
            std_err = self.ioHandler.getStderr()
            
            if ROOT.gPad:
                 if ROOT.gPad.IsDrawn():
                     canvaslist = ROOT.gROOT.GetListOfCanvases()
                     for canvas in canvaslist:
                          canvas.Draw()
                          if canvas.IsDrawn():
                               self.drawer = CanvasDrawer(canvas)
                               if self.drawer._canJsDisplay():
                                    display(HTML(self.drawer.jsCode()))
                               else:
                                    display(self.drawer.pngImg())
                               canvas.ResetDrawn()
        
            
        except KeyboardInterrupt:
            self.interpreter.gROOT.SetInterrupt()
            status = 'interrupted'
            self.ioHandler.EndCapture()
            std_out = self.ioHandler.getStdout()
            std_err = self.ioHandler.getStderr()
        if not silent:
            ## Send output on stdout
            stream_content_stdout = {'name': 'stdout', 'text': std_out}
            self.send_response(self.iopub_socket, 'stream', stream_content_stdout)
            if std_err != "":
                stream_content_stderr = {'name': 'stderr', 'text': std_err}
                self.send_response(self.iopub_socket, 'stream', stream_content_stderr)
            
        reply = {'status': status,
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
                }

        if status == 'interrupted':
            pass
        elif status == 'error':
            err = {
                'ename': 'ename',
                'evalue': 'evalue',
                'traceback': traceback,
            }
            self.send_response(self.iopub_socket, 'error', err)
            reply.update(err)
        elif status == 'ok':
            pass
        else:
            raise ValueError("Invalid status: %r" % status)
        #return reply

def main():
    """launch a root kernel"""
    try:
        from ipykernel.kernelapp import IPKernelApp
    except ImportError:
        from IPython.kernel.zmq.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=ROOTKernel)

if __name__ == '__main__':
    main()