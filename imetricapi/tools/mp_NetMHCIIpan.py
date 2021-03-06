from .LocalNetMHCbase import LocalNetMHCPeptidePredictor

def get_instance(config):
    #if IEDB locally installed
    return LocalNetMHCIIPanPredictor(**config.get_section("NetMHCIIpan"))
    #else
    #   return WebNetMHCIIPanPredictor(config)

class LocalNetMHCIIPanPredictor(LocalNetMHCPeptidePredictor):
    """MHCPeptidePredictor that calls a locally installed 
    netMHCIIpan instance."""
    
    def init(self):
        self.attr["mhc"] = (2,)
        self.attr.setdefault("executable", "netMHCIIpan")
        self.attr.setdefault("tempdir", None)
        
    def reformat_alleles(self, alleles):
        return list(allele.split("-")[1].replace("*", "_") for allele in alleles)
    
    def _get_predict_command(self, executable, seq_file, lengths_str, allele):
        return [
            executable, 
            "-length", lengths_str, 
            "-a", allele, 
            "-f", seq_file,
            "-tdir", self.tempdir
        ]
    
    def _reformat_DataFrame(self, df):
        return df.drop([4,5,6,9,10,11], 1)
        
    def _get_list_command(self, executable):
        return [executable, "-list"]
