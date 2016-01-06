import csv
import os
import pandas as pd
import subprocess

from imetricapi.predict import MHCPeptidePredictor
from imetricapi.util import create_temp_fasta, sort_by_length, rbind, check_executable

class LocalNetMHCPeptidePredictor(MHCPeptidePredictor):
    def can_execute(self):
        return check_executable(self.executable)
    
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
        lengths_str = ",".join(map(str, lengths))
        seq_file = create_temp_fasta(sequences, self.tempdir)
        
        def _exec(allele):
            cmd = self._get_predict_command(
                self.executable, seq_file, lengths_str, allele)
            output = subprocess.check_output(cmd, universal_newlines=True)
            return self._parse_predict_output(output)
        
        try:
            return list(_exec(allele) for allele in alleles)
        
        finally:
            os.remove(seq_file)
    
    def _parse_predict_output(self, output):
        headers = []
        summaries = []
        rows = []
        div_count = 0
        
        for row in output.split("\n"):
            if row.startswith("-"):
                # we found a table divider row
                div_count += 1
            elif div_count == 0:
                # we're before the table
                headers.append(row)
            elif div_count == 1:
                # this is the header - ignore
                pass
            elif div_count == 2:
                # we're in the main body of the table
                rows.append(row)
            else:
                # we're after the table
                summaries.append(row)
        
        return (
            list(csv.reader(rows, delimiter=" ", skipinitialspace=True)),
            headers, 
            summaries
        )
    
    def _prepare_DataFrame(self, rows_list):
        df = rbind(rows_list)
        df = self._reformat_DataFrame(df)
        df.columns = [
            "pos", "allele", "peptide", "identity", 
            "1-log50k(aff)", "affinity"
        ]
        df["pos"] = pd.to_numeric(df["pos"], errors='coerce')
        df["1-log50k(aff)"] = pd.to_numeric(df["1-log50k(aff)"], errors='coerce')
        df["affinity"] = pd.to_numeric(df["affinity"], errors='coerce')
        df = df.dropna()
        df["rank"] = df["affinity"].rank(method="min", ascending=1)
        return df
    
    def listMHCAlleles(self):
        """Get available alleles"""
        cmd = self._get_list_command(self.executable)
        output = subprocess.check_output(cmd, universal_newlines=True)
        alleles = []
        for row in output.split("\n"):
            if row.startswith("#") or len(row.strip()) == 0:
                continue
            alleles.append(row)
        return alleles
        