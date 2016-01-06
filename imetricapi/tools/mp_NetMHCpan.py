import csv
from .LocalNetMHCbase import LocalNetMHCPeptidePredictor

def get_instance(config):
    #if IEDB locally installed
    return LocalNetMHCPanPredictor(**config.get_section("NetMHCpan"))
    #else
    #   return WebNetMHCIIPanPredictor(config)

class LocalNetMHCPanPredictor(LocalNetMHCPeptidePredictor):
    """MHCPeptidePredictor that calls a locally installed 
    netMHCpan instance."""
    
    def init(self):
        self.attr["mhc"] = (1,)
        self.attr.setdefault("executable", "netMHCpan")
        self.attr.setdefault("tempdir", None)
    
    def reformat_alleles(self, alleles):
        return list(allele.replace("*", "_") for allele in alleles)
    
    def _get_predict_command(self, executable, seq_file, lengths_str, allele):
        return [
            executable, 
            "-l", lengths_str, 
            "-a", allele, 
            "-f", seq_file,
            "-tdir", self.tempdir
        ]
    
    def _reformat_DataFrame(self, df):
        return df.drop([6], 1)
    
    def _get_list_command(self, executable):
        return [executable, "-listMHC"]
