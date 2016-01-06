import json
import io
import pandas as pd
import requests

class WebIEDBbase(object):
    def init(self):
        # subclasses should define url and method at a minimum:
        # self.attr["url"] = xxx
        # self.attr["method"] = xxx
        pass
    
    def getPeptidePredictions(self, sequences, alleles, species, **kwargs):
        df = None
        for sequence in sequences:
            length_str = len(sequence)
            for allele in alleles:
                data = {
                    "sequence_text": sequence,
                    "length": length_str,
                    "method": self.method,
                    "allele": allele,
                }
                temp = self._predict(data)
                if df is None:
                    df = temp
                else:
                    df = df.append(temp, ignore_index=True)
        return df
    
    def getProteinPredictions(self, sequences, lengths, alleles, species, **kwargs):
        df = None
        for sequence in sequences:
            length_str = ",".join(str(l) for l in lengths)
            for allele in alleles:
                data = {
                    "sequence_text": sequence,
                    "length": length_str,
                    "method": self.method,
                    "allele": allele,
                }
                temp = self._predict(data)
                if df is None:
                    df = temp
                else:
                    df = df.append(temp, ignore_index=True)
        return df
    
    def _predict(self, data):
        response = requests.post(self.url, data=data)
        if response.ok:
            return self._parse_response(response.text)
        else:
            raise Exception() # TODO
    
    def _parse_response(self, response):
        df = None
        for sequence, data in json.loads(response).items():
            temp = pd.read_csv(io.StringIO(data.values()[0]), sep="\t")
            if df is None:
                df = temp
            else:
                df = df.append(temp, ignore_index=True)
                
        to_rename = set(df.columns) - set("allele","peptide")
        if len(to_rename) > 0:
            df = df.rename(dict((col, "{0}_{1}".format(name, col)) 
        
        return df
    
    def listMHCAlleles(self):
        raise NotImplemented()
