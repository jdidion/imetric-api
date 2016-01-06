from imetricapi.predict import MHCImmunoPredictor
from imetricapi.util import create_temp_fasta, check_executable
import os
import subprocess
import pandas as pd

def get_instance(config):
    #if IEDB locally installed
    return LocalIEDBImmunPredictor(**config.get_section("IEDBImmun"))
    #else
    #   return WebNetMHCIIPanPredictor(config)

class LocalIEDBImmunPredictor(MHCImmunoPredictor):
    """IEDBImmunoPredictor that calls a locally installed 
    IEDB Immunogenicity tool."""
    
    def init(self, **kwargs):
        self.attr.setdefault("executable", "predict_immunogenicity.py")
        self.attr.setdefault("tempdir", None)
    
    def can_execute(self):
        return check_executable(self.executable)
    
    def getEpitopePredictions(self, sequences):
        rows = self._predict(sequences)
        return self._prepare_DataFrame(rows_list)
    
    def _predict(self, sequences):
        print("Hello in _predict");
        print(sequences)
        
        seq_file = create_temp_fasta(sequences, self.tempdir)

        try:
            return list(self._execute(seq_file))

        finally:
            os.remove(seq_file)
    
    def _execute(self, seq_file):
        cmd = [
            self.executable, 
            seq_file
        ]
        print(cmd)
        output = subprocess.check_output(cmd)
        output = output.split("\n")[1:]
        return output
    
    def _prepare_DataFrame(self, rows_list):
        df = rbind(rows_list)
        df.columns = [
            "peptide", "length", "score"
        ]            
        df = df.convert_objects(convert_numeric=True)
        df = df.drop(["length"], 1)
        df = df.dropna()
