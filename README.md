# imetric-api

IMETRIC (Immunogenicity METa pRedICtion) is a web framework for running MHC:peptide binding and immunogenicity prediction tools (TODO: link to IMETRIC GitHub repo). This library provide the python API that IMETRIC uses to call those prediction tools. There is also a script to run the tools from the command line.

The IMETRIC API was originally based on MHCpredict: https://github.com/dmnfarrell/mhcpredict

# Usage

Generate MHC:peptide binding predictions for every available MHC allele in every supported database.

```python
result = imetricapi.predict.predictPeptides("VIFRLMRTNFL")
```

# To evaluate

* http://boson.research.microsoft.com/bio/epipred.aspx