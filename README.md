# imetric-api

IMETRIC (Immunogenicity METa pRedICtion) is a web framework for running MHC:peptide binding and immunogenicity prediction tools (TODO: link to IMETRIC GitHub repo). This library provide the python API that IMETRIC uses to call those prediction tools. There is also a script to run the tools from the command line.

The IMETRIC API was originally based on MHCpredict: https://github.com/dmnfarrell/mhcpredict

# A Note on FRED-2

Recently, a similar API was published in Bioinformatics: https://github.com/FRED-2/Fred2. We will consider using FRED-2 as the backend for iMetric, and contributing any code from our API that might improve FRED-2.

# Usage

Generate MHC:peptide binding predictions for every available MHC allele in every supported database.

```python
result = imetricapi.predict.predictPeptides("VIFRLMRTNFL")
```

# TODO

* Refactor ToolLoader to be able to load modules from third-party packages.

# To evaluate

* http://boson.research.microsoft.com/bio/epipred.aspx
