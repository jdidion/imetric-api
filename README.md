# imetric-api

IMETRIC (Immunogenicity METa pRedICtion) is a web framework for running MHC:peptide binding and immunogenicity prediction tools (TODO: link to IMETRIC GitHub repo). This library provide the python API that IMETRIC uses to call those prediction tools. There is also a script to run the tools from the command line.

# Usage

Generate MHC:peptide binding predictions for every available MHC allele in every supported database.

```python
result = imetricapi.predict.predictPeptides("VIFRLMRTNFL")
```
