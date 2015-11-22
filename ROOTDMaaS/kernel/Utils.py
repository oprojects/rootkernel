import sys
import os
from glob import glob
import __builtin__


from ROOTDMaaS.io import Handler


_ioHandler = None
_Executor = None
_Declarer = None

def GetIOHandler():
    global _ioHandler
    if not _ioHandler:
        Handler.LoadHandlers()
        from ROOT import ROOTDMSaaSExecutorHandler
        _ioHandler = ROOTDMSaaSExecutorHandler()
    return _ioHandler
    
def GetExecutor():
    global _Executor
    if not _Executor:
        from ROOT import ROOTDMaaSExecutor
        _Executor = ROOTDMaaSExecutor
    return _Executor

def GetDeclarer():
    global _Declarer
    if not _Declarer:
        from ROOT import ROOTDMaaSDeclarer
        _Declarer = ROOTDMaaSDeclarer
    return _Declarer


class MagicLoader(object):
    '''Class to load ROOTDMaaS Magics'''
    def __init__(self,kernel):        
         magics_path = os.path.dirname(__file__)+"/../magics/*.py"
         for file in glob(magics_path):
              if file != magics_path.replace("*.py","__init__.py"):
                  module_path="ROOTDMaaS.magics."+file.split("/")[-1].replace(".py","")
                  module= __builtin__.__import__(module_path, globals(), locals(), ['register_magics'], -1)
                  module.register_magics(kernel)




    