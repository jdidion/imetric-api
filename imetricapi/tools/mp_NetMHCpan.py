import csv
from .NetMHCbase import NetMHCPeptidePredictor

def get_instance(config):
    #if IEDB locally installed
    return LocalNetMHCPanPredictor(**config.get_section("NetMHCpan"))
    #else
    #   return WebNetMHCIIPanPredictor(config)

class LocalNetMHCPanPredictor(NetMHCPeptidePredictor):
    """MHCPeptidePredictor that calls a locally installed 
    netMHCpan instance."""
    
    def init(self, executable="netMHCpan", tempdir=None, **kwargs):
        NetMHCPeptidePredictor.init(self, executable, tempdir, **kwargs)
    
    def _reformat_alleles(self, alleles):
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
        df.drop([3,6], 1)
        return df
    
    def _get_list_command(self, executable):
        return [executable, "-listMHC"]
