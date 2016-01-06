import json
import io
import pandas as pd
import requests
import numpy as np
import scipy as sp

def post_to_iedb_mhci(protein_sequence, method='smm', length='9', allele='HLA-A*01:01'):
    data = {
        'sequence_text': protein_sequence,
        'length': length,
        'method': method,
        'allele': allele,
    }
    url = 'http://tools-api.iedb.org/tools_api/mhci/'
    response = requests.post(url, data=data)
    if response.ok:
        return response.text
    else:
        return 'Something went wrong'


def procIEDB(request):
   j = json.loads(request.text)
   h = j[j.keys()[0]]
   i = h.values()[0]
   o = io.StringIO(i)
   d = pd.read_csv(o, sep='\t')
   i = h.values()[1]
   o = io.StringIO(i)
   d1 = pd.read_csv(o, sep='\t')
   return(d,d1)