# -*- coding:utf-8 -*-
#-----------------------------------------------------------------------------
#  Copyright (c) 2015, ROOT Team.
#  
#  Authors: Danilo Piparo <Danilo.Piparo@cern.ch> CERN
#           Enric Tejedor enric.tejedor.saavedra@cern.ch> CERN
#  Modified by: Omar Zapata <Omar.Zapata@cern.ch> http://oproject.org
#  website: http://oproject.org/ROOT+Jupyter+Kernel (information only for ROOT kernel)
#  Distributed under the terms of the Modified BSD License.
#
#  The full license is in the file COPYING.rst, distributed with this software.
#-----------------------------------------------------------------------------

import sys
import tempfile
import fnmatch
from contextlib import contextmanager

import IPython.display
from metakernel.display import display,HTML
import ROOT

_jsDefaultHighlight = """
// Set default mode for code cells
IPython.CodeCell.options_default.cm_config.mode = '{mimeType}';
// Set CodeMirror's current mode
var cells = IPython.notebook.get_cells();
cells[cells.length-1].code_mirror.setOption('mode', '{mimeType}');
// Set current mode for newly created cell
cells[cells.length-1].cm_config.mode = '{mimeType}';
"""

_jsMagicHighlight = "IPython.CodeCell.config_defaults.highlight_modes['magic_{cppMIME}'] = {{'reg':[/^%%cpp/]}};"


_jsNotDrawableClassesPatterns = ["TGraph[23]D","TH3*","TGraphPolar","TProf*","TEve*","TF[23]","TGeo*","TPolyLine3D"]


_jsROOTSourceDir = "https://root.cern.ch/js/dev/"
_jsCanvasWidth = 800
_jsCanvasHeight = 600

_jsCode = """
<div id="{jsDivId}"
     style="width: {jsCanvasWidth}px; height: {jsCanvasHeight}px">
</div>
<script>
requirejs.config(
{{
  paths: {{
    'JSRootCore'    : '{jsROOTSourceDir}/scripts/JSRootCore',
    'JSRootPainter' : '{jsROOTSourceDir}/scripts/JSRootPainter',
  }}
}}
);
require(['JSRootCore', 'JSRootPainter'],
        function(Core, Painter) {{
          var obj = Core.parse('{jsonContent}');
          Painter.draw("{jsDivId}", obj, "{jsDrawOptions}");
        }}
);
</script>
"""

_enableJSVis = False
_enableJSVisDebug = False
def enableJSVis():
    global _enableJSVis
    _enableJSVis = True

def disableJSVis():
    global _enableJSVis
    _enableJSVis = False

def enableJSVisDebug():
    global _enableJSVis
    global _enableJSVisDebug
    _enableJSVis = True
    _enableJSVisDebug = True

def disableJSVisDebug():
    global _enableJSVis
    global _enableJSVisDebug
    _enableJSVis = False
    _enableJSVisDebug = False


@contextmanager
def _setIgnoreLevel(level):
    originalLevel = ROOT.gErrorIgnoreLevel
    ROOT.gErrorIgnoreLevel = level
    yield
    ROOT.gErrorIgnoreLevel = originalLevel

class CanvasDrawer(object):
    '''
    Capture the canvas which is drawn and decide if it should be displayed using
    jsROOT.
    '''
    jsUID = 0

    def __init__(self, canvas):
        self.canvas = canvas

    def _getListOfPrimitivesNamesAndTypes(self):
       """
       Get the list of primitives in the pad, recursively descending into
       histograms and graphs looking for fitted functions.
       """
       primitives = self.canvas.GetListOfPrimitives()
       primitivesNames = map(lambda p: p.ClassName(), primitives)
       #primitivesWithFunctions = filter(lambda primitive: hasattr(primitive,"GetListOfFunctions"), primitives)
       #for primitiveWithFunctions in primitivesWithFunctions:
       #    for function in primitiveWithFunctions.GetListOfFunctions():
       #        primitivesNames.append(function.GetName())
       return sorted(primitivesNames)

    def _getUID(self):
        '''
        Every DIV containing a JavaScript snippet must be unique in the
        notebook. This methods provides a unique identifier.
        '''
        CanvasDrawer.jsUID += 1
        return CanvasDrawer.jsUID

    def _canJsDisplay(self):
        # to be optimised
        if not _enableJSVis: return False
        primitivesTypesNames = self._getListOfPrimitivesNamesAndTypes()
        for unsupportedPattern in _jsNotDrawableClassesPatterns:
            for primitiveTypeName in primitivesTypesNames:
                if fnmatch.fnmatch(primitiveTypeName,unsupportedPattern):
                    print >> sys.stderr, "The canvas contains an object of a type jsROOT cannot currently handle (%s). Falling back to a static png." %primitiveTypeName
                    return False
        return True

    def _jsDisplay(self):
        # Workaround to have ConvertToJSON work
        json = ROOT.TBufferJSON.ConvertToJSON(self.canvas, 3)
        #print "JSON:",json

        # Here we could optimise the string manipulation
        divId = 'root_plot_' + str(self._getUID())
        thisJsCode = _jsCode.format(jsCanvasWidth = _jsCanvasWidth,
                                    jsCanvasHeight = _jsCanvasHeight,
                                    jsROOTSourceDir = _jsROOTSourceDir,
                                    jsonContent=json.Data(),
                                    jsDrawOptions="",
                                    jsDivId = divId)

        # display is the key point of this hook
        display(HTML(thisJsCode))

    def JsCode(self):
        # Workaround to have ConvertToJSON work
        json = ROOT.TBufferJSON.ConvertToJSON(self.canvas, 3)
        #print "JSON:",json

        # Here we could optimise the string manipulation
        divId = 'root_plot_' + str(self._getUID())
        thisJsCode = _jsCode.format(jsCanvasWidth = _jsCanvasWidth,
                                    jsCanvasHeight = _jsCanvasHeight,
                                    jsROOTSourceDir = _jsROOTSourceDir,
                                    jsonContent=json.Data(),
                                    jsDrawOptions="",
                                    jsDivId = divId)

        # display is the key point of this hook
        return thisJsCode


    def _pngDisplay(self):
        ofile = tempfile.NamedTemporaryFile(suffix=".png")
        with _setIgnoreLevel(ROOT.kError):
            self.canvas.SaveAs(ofile.name)
        img = IPython.display.Image(filename=ofile.name, format='png', embed=True)
        display(img)

    def PngImage(self):
        ofile = tempfile.NamedTemporaryFile(suffix=".png")
        with _setIgnoreLevel(ROOT.kError):
            self.canvas.SaveAs(ofile.name)
        img = IPython.display.Image(filename=ofile.name, format='png', embed=True)
        return img

    def _display(self):
       if _enableJSVisDebug:
          self._pngDisplay()
          self._jsDisplay()
       else:
         if self._canJsDisplay():
            self._jsDisplay()
         else:
            self._pngDisplay()


    def Draw(self):
        self._display()
        return 0

def _PyDraw(thePad):
   """
   Invoke the draw function and intercept the graphics
   """
   drawer = CanvasDrawer(thePad)
   drawer.Draw()

def setStyle():
    style=ROOT.gStyle
    style.SetFuncWidth(3)
    style.SetHistLineWidth(3)
    style.SetMarkerStyle(8)
    style.SetMarkerSize(.5)
    style.SetMarkerColor(ROOT.kBlue)
    style.SetPalette(57)
    
def LoadDrawer():
    setStyle()
    ROOT.enableJSVis = enableJSVis
    ROOT.disableJSVis = disableJSVis
    ROOT.enableJSVisDebug = enableJSVisDebug
    ROOT.disableJSVisDebug = disableJSVisDebug
    ROOT.TCanvas.DrawCpp = ROOT.TCanvas.Draw
    ROOT.TCanvas.Draw = _PyDraw
