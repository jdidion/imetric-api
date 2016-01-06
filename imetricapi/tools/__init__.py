import configparser
import glob
import importlib
import os
import sys

import imetricapi
import imetricapi.util

def get_MHCPeptidePredictors(names=None, mhc_class=None, config=None):
    predictors = _get_predictors("mp", names, config)
    if mhc_class is not None:
        predictors = { k:v for (k,v) in predictors.items() if v.supports_class(mhc_class) }
    return predictors

def get_MHCImmunoPredictors(names=None, config=None):
    return _get_predictors("ep", names, config)

def _get_predictors(predictor_type, names, config):
    predictors = ToolLoader(predictor_type).get_predictors(names, config)
    predictors = { k:v for (k,v) in predictors.items() if v.can_execute() }
    return predictors

class ToolLoader(object):
    def __init__(self, prefix):
        self.prefix = prefix
        self.all_modules = None
    
    def get_predictors(self, names=None, config=None):
        """Create a predictor for each name given, or create instances
        of all available predictors if 'names' is None.
    
        Args:
            names: list of predictor names.
            config: ConfigParser instance, or path to config file.
    
        Returns:
            A list of MHCPeptidePredictors
        """
        if config is None:
            config = imetricapi.util.DictConfig()
        
        modules = self.get_modules()
    
        if names is None:
            names = modules.keys()
    
        elif isinstance(names, str):
            names = [names]
    
        def create_predictor(name):    
            if name in modules:
                mod = modules[name]
                return mod.get_instance(config)
        
            else:
                raise Exception("No such predictor {}".format(name))
    
        return dict((name, create_predictor(name)) for name in names)

    def get_modules(self):
        if self.all_modules is None:
            
            mod_dir = os.path.join(
                os.path.dirname(os.path.abspath(imetricapi.__file__)), 
                "tools"
            )
            
            #if sys.version_info >= (3, 4):
            #    import importlib.util
            #    spec = importlib.util.find_spec("imetricapi.tools")
            #    mod_dir = spec.submodule_search_locations[0]
            
            #elif sys.version_info < (3, 0):
            #    import imp
            #    file, mod_dir, description = imp.find_module("tools", )
                
            mod_names = set(map(
                lambda path: os.path.splitext(os.path.basename(path))[0], 
                glob.glob(os.path.join(mod_dir, "{}_*.py*".format(self.prefix)))
            ))
            self.all_modules = dict((
                    mod_name[(len(self.prefix)+1):], 
                    importlib.import_module("."+mod_name, package="imetricapi.tools")
                )
                for mod_name in mod_names)

        return self.all_modules
