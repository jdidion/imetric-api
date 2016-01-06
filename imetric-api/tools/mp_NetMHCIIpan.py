from imetricapi.predict import MHCPeptidePredictor
from imetricapi.util import create_temp_fasta, sort_by_length, rbind
import os
import re
import subprocess

def get_instance(config):
    #if IEDB locally installed
    return LocalNetMHCIIPanPredictor(**config.get_section("NetMHCIIpan"))
    #else
    #   return WebNetMHCIIPanPredictor(config)

class LocalNetMHCIIPanPredictor(MHCPeptidePredictor):
    """MHCPeptidePredictor that calls a locally installed 
    netMHCIIpan instance."""
    
    def init(self, executable="netMHCIIpan", tempdir=None, **kwargs):
        NetMHCPeptidePredictor.init(self, executable, tempdir, **kwargs)
    
    def _reformat_alleles(self, alleles):
        return list(allele.split("-")[1].replace("*", "_") for allele in alleles)
    
    def _get_command(self, executable, seq_file, lengths_str, allele):
        return [
            executable, 
            "-length", lengths_str, 
            "-a", allele, 
            "-f", seq_file,
            "-tdir", self.tempdir
        ]

    def _parse_output(self, output):
        pass
    
    def _prepare_DataFrame(self, rows_list):
        df = rbind(rows_list)
        df.colnames = [
            "pos", "allele", "peptide", "identity", "pos", 
            "core", "1-log50k(aff)", "affinity", "rank"
        ]
        df = df.drop(["pos", "identity", "rank"], 1)
        pd.to_numeric(df[:,"pos"], errors='coerce')
        pd.to_numeric(df[:,"1-log50k(aff)"], errors='coerce')
        pd.to_numeric(df[:,"affinity"], errors='coerce')
        df = df.dropna()
        df["rank"] = df["affinity"].rank(method="min", ascending=1)
        return df
    
    def listMHCAlleles(self):
        """Get available alleles"""
        cmd = [self.executable, "-list"]
        temp = subprocess.check_output(cmd)
        alleles = temp.split("\n")[34:]
        return alleles
