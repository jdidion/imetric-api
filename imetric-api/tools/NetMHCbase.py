
class NetMHCPeptidePredictor(MHCPeptidePredictor):
    def init(self, executable, tempdir, **kwargs):
        self.executable = executable
        self.tempdir = tempdir
    
    def getPeptidePredictions(self, sequences, alleles, species):
        if len(sequences) == 0 or len(alleles) == 0:
            # TODO: warn
            return None
        seq_lengths = sort_by_length(sequences)
        results = []
        for seq_len, seqs in seq_lengths.items():
            results.extend(self._predict(seqs, [seq_len], alleles, species))
        return self._prepare_DataFrame(list(result[0] for result in results))
    
    def getProteinPredictions(self, sequences, lengths, alleles, species):
        if len(sequences) == 0 or len(alleles) == 0:
            # TODO: warn
            return None
        results = self._predict(sequences, lengths, alleles, species)
        return self._prepare_DataFrame(list(result[0] for result in results))
    
    def _predict(self, sequences, lengths, alleles, species):
        alleles = self._reformat_alleles(alleles)
        lengths = ",".join(map(str, lengths))
        seq_file = create_temp_fasta(sequences, self.tempdir)
        
        try:
            return list(self._execute(seq_file, lengths, allele)
                for allele in alleles)
        finally:
            #os.remove(seq_file)
            pass
    
    def _execute(self, seq_file, lengths_str, allele):
        cmd = self._get_command(self.executable, seq_file, lengths_str, allele)
        output = subprocess.check_output(cmd)
        return self.parse_output(output)