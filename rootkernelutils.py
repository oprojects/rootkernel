import ROOT
import sys, os, select
from contextlib import contextmanager

# Here functions are defined to process C++ code
def processCppCodeImpl(code):
    #code = commentRemover(code)
    ROOT.gInterpreter.ProcessLine(code)

def declareCppCodeImpl(code):
    #code = commentRemover(code)
    ROOT.gInterpreter.Declare(code)

def processCppCode(code):
    processCppCodeImpl(code)

def declareCppCode(code):
    declareCppCodeImpl(code)

@contextmanager
def _setIgnoreLevel(level):
    originalLevel = ROOT.gErrorIgnoreLevel
    ROOT.gErrorIgnoreLevel = level
    yield
    ROOT.gErrorIgnoreLevel = originalLevel


class StreamCapture(object):
    def __init__(self, stream):
        streamsFileNo={sys.stderr:2,sys.stdout:1}
        self.pipe_out = None
        self.pipe_in = None
        self.sysStreamFile = stream
        self.sysStreamFileNo = streamsFileNo[stream]
        # Platform independent flush
        # With ctypes, the name of the libc library is not known a priori
        # We use jitted function
        flushFunctionName='_ROOTaaS_Flush'
        if (not hasattr(ROOT,flushFunctionName)):
           declareCppCode("void %s(){fflush(nullptr);};" %flushFunctionName)
        self.flush = getattr(ROOT,flushFunctionName)


    def more_data(self):
        r, _, _ = select.select([self.pipe_out], [], [], 0)
        return bool(r)

    def pre_execute(self):
        self.pipe_out, self.pipe_in = os.pipe()
        os.dup2(self.pipe_in, self.sysStreamFileNo)

    def post_execute(self):
        out = ''
        if self.pipe_out:
            while self.more_data():
                out += os.read(self.pipe_out, 1024)

        self.flush()
        self.sysStreamFile.write(out) # important to print the value printing output
        return out

def rreplace(s, old, new, occurrence):
  li = s.rsplit(old, occurrence)
  return new.join(li)

# Jit a wrapper for the ttabcom
_TTabComHookCode = """
std::vector<std::string> _TTabComHook(const char* pattern){
  static auto ttc = new TTabCom;
  int pLoc = strlen(pattern);
  std::ostringstream oss;
  ttc->Hook((char* )pattern, &pLoc, oss);
  std::stringstream ss(oss.str());
  std::istream_iterator<std::string> vbegin(ss), vend;
  return std::vector<std::string> (vbegin, vend);
}
"""

class CppCompleter(object):
    '''
    Completer which interfaces to the TTabCom of ROOT. It is activated
    (deactivated) upon the load(unload) of the load of the extension.

    >>> comp = CppCompleter()
    >>> comp.activate()
    >>> for suggestion in comp._completeImpl("TH1"):
    ...     print suggestion
    TH1
    TH1C
    TH1D
    TH1F
    TH1I
    TH1K
    TH1S
    >>> for suggestion in comp._completeImpl("TH2"):
    ...     print suggestion
    TH2
    TH2C
    TH2D
    TH2F
    TH2GL
    TH2I
    TH2Poly
    TH2PolyBin
    TH2S
    >>> garbage = ROOT.gInterpreter.ProcessLine("TH1F* h")
    >>> for suggestion in comp._completeImpl("h->GetA"):
    ...     print suggestion
    h->GetArray
    h->GetAsymmetry
    h->GetAt
    h->GetAxisColor
    >>> for suggestion in comp._completeImpl("TROOT::Is"):
    ...     print suggestion
    IsA
    IsBatch
    IsEqual
    IsEscaped
    IsExecutingMacro
    IsFolder
    IsInterrupted
    IsLineProcessing
    IsModified
    IsOnHeap
    IsProofServ
    IsRootFile
    IsSortable
    IsWritable
    IsZombie
    >>> comp.deactivate()
    >>> for suggestion in comp._completeImpl("TG"):
    ...     print suggestion
    '''

    def __init__(self):
        self.hook = None
        self.active = True
        self.firstActivation = True
        self.accessors = [".", "->", "::"]

    def activate(self):
        self.active = True
        if self.firstActivation:
            declareCppCode('#include "dlfcn.h"')
            dlOpenRint = 'dlopen("libRint.so",RTLD_NOW);'
            processCppCode(dlOpenRint)
            declareCppCode(_TTabComHookCode)
            self.hook = ROOT._TTabComHook
            self.firstActivation = False

    def deactivate(self):
        self.active = False

    def _getSuggestions(self,line):
        if self.active:
            return self.hook(line)
        return []

    def _getLastAccessorPos(self,line):
        accessorPos = -1
        for accessor in self.accessors:
            tmpAccessorPos = line.rfind(accessor)
            if accessorPos < tmpAccessorPos:
                accessorPos = tmpAccessorPos+len(accessor) if accessor!="::" else 0
        return accessorPos

    def _completeImpl(self, line):
        line=line.split()[-1]
        suggestions = self._getSuggestions(line)
        if not suggestions: return []
        accessorPos = self._getLastAccessorPos(line)
        suggestions = sorted(suggestions)
        if accessorPos > 0:
            suggestions = [line[:accessorPos]+sugg for sugg in suggestions]
        return suggestions

    def complete(self, ip, event) :
        '''
        Autocomplete interfacing to TTabCom. If an accessor of a scope is
        present in the line, the suggestions are prepended with the line.
        That's how completers work. For example:
        myGraph.Set<tab> will return "myGraph.Set+suggestion in the list of
        suggestions.
        '''
        return self._completeImpl(event.line)



