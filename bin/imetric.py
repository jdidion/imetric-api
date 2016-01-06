#!/usr/bin/env python

import imetricapi.predict
import imetricapi.util

if __name__ == "__main__":
    result = imetricapi.predict.predictPeptides(
        "VIFRLMRTNFL", 
        alleles="HLA-DRB1*0101",
        methods=["NetMHCpan"],
        config=imetricapi.util.DictConfig(dict(NetMHCpan=dict(
            executable="/Users/didionjp/Downloads/netMHCIIpan-3.1/netMHCIIpan",
            tempdir=".")))
    )
    result.to_csv("output.txt", sep="\t")
    
import imetricapi.predict
import imetricapi.util    
result = imetricapi.predict.predictProteins(
    "VIFRLMRTNFL",
    lengths=(9,),
    alleles="HLA-DRB1*0101",
    methods=["NetMHCIIpan"],
    config=imetricapi.util.DictConfig(dict(NetMHCIIpan=dict(
        executable="/Users/didionjp/Downloads/netMHCIIpan-3.1/netMHCIIpan",
        tempdir=".")))
)

import imetricapi.predict
import imetricapi.util    
result = imetricapi.predict.predictProteins(
    "VIFRLMRTNFL",
    lengths=(9,),
    alleles="HLA-A01:01",
    methods=["NetMHCpan"],
    config=imetricapi.util.DictConfig(dict(NetMHCpan=dict(
        executable="/home/ubuntu/software/netMHCpan-2.8/Linux_x86_64/bin/netMHCpan",
        tempdir="/home/ubuntu/software/Epitopes_from_TCRs/mhcpredict")))
)

import imetricapi.predict
import imetricapi.util    
result = imetricapi.predict.predictEpitopes("VIFRLMRTNFL")