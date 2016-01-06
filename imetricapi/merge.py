import pandas as pd

def merge_tables(results, data_columns=["affinity"]):
    """Merge the prediction results from multiple tools. Returns a table
    With peptide, allele, mhc_class as the first three columns, and 
    additional columns for each tool.
    """
    
    df = None
    for name, info in results.items():
        data = info["result"]
        
        tool_type = "mhcI" if info["mhc"] == (1,) else "mhcII"
        data["mhc_class"] = pd.Series(tool_type, index=data.index)
        
        header_cols = ["peptide", "allele", "mhc_class"]
        
        if data_columns is None:
            data_columns = data.columns - set(header_cols)
        
        else:
            to_keep = header_cols + data_columns
            to_drop = set(data.columns) - set(to_keep)
            data = data.drop(to_drop, 1)
        
        data = data[header_cols + data_columns]
        
        to_rename = set(data.columns) - set(header_cols)
        data = data.rename(columns=dict((col, "{0}_{1}".format(name, col))
            for col in to_rename))
        
        if df is None:
            df = data
        else:
            df = pd.merge(df, data, on=header_cols, how="outer")
    
    return df
