#!/usr/bin/env python

from __future__ import print_function

import sys, os, select, tempfile

#ROOT related imports
import ROOT
from ROOTaaS.iPyROOT import utils 
from ROOTaaS.iPyROOT.cppcompleter import CppCompleter


import IPython

from metakernel import MetaKernel
from metakernel.display import clear_output, display, HTML

from rootkernelutils import StreamCapture, CanvasDrawer
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
        self._stderr = StreamCapture(sys.stderr)
        self._stdout = StreamCapture(sys.stdout)
        self.completer = CppCompleter()
        self.completer.activate()
        self.drawer_capturer = utils.CaptureDrawnCanvases()

    def get_completions(self, info):
        if _debug :Debug(info)
        return self.completer._completeImpl(info['code'])
      
    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):        
        status = 'ok'
        traceback = None
        std_out=""
        std_err=""
        try:
            self._stdout.pre_execute();
            if not _debug : self._stderr.pre_execute();
            root_status = ROOT.gROOT.ProcessLine(code)
            self._stdout.flush()
            if not _debug : self._stderr.flush()
            std_out = self._stdout.post_execute()
            if not _debug : std_err = self._stderr.post_execute()
            if ROOT.gPad:
	         if ROOT.gPad.IsDrawn():
                     self.drawer = CanvasDrawer(ROOT.gPad)
                     if self.drawer._canJsDisplay():
                         display(HTML(self.drawer.jsCode()))
                     else:
                         display(self.drawer.pngImg())
            self.drawer_capturer._post_execute()
            
        except KeyboardInterrupt:
            self.interpreter.gROOT.SetInterrupt()
            status = 'interrupted'
            std_out = self._stdout.post_execute();
            if not _debug : std_err = self._stderr.post_execute();
        if not silent:
            ## Send output on stdout
            #stream_content_stdout = {'name': 'stdout', 'text': stdout}
            #self.send_response(self.iopub_socket, 'stream', stream_content_stdout)
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
        return reply

def main():
    """launch a root kernel"""
    try:
        from ipykernel.kernelapp import IPKernelApp
    except ImportError:
        from IPython.kernel.zmq.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=ROOTKernel)

if __name__ == '__main__':
    main()