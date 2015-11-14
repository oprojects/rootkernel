
import sys
import os
from glob import glob
import __builtin__

class MagicLoader(object):
    '''Class to load ROOTDMaaS Magics'''
    def __init__(self,kernel):        
         magics_path = os.path.dirname(__file__)+"/ROOTDMaaS/Magics/*.py"
         for file in glob(magics_path):
              if file != magics_path.replace("*.py","__init__.py"):
                  module_path="ROOTDMaaS.Magics."+file.split("/")[-1].replace(".py","")
                  module= __builtin__.__import__(module_path, globals(), locals(), ['register_magics'], -1)
                  module.register_magics(kernel)


