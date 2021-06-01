##################################################################
# get-snp.py
# Retrieves and collates all the single nucleotide polymorphisms
# present in given genes.
# Author: Bryon Drown (Northwestern University)
# Created: July 22, 2020
#
# Usage: python get-snp.py [Directory with MAFs] [Genes to search]
# Generates: merged.csv file in the directory with MAFs
##################################################################

import argparse
import sys
import os
import pandas as pd
import glob

__doc__ = """Tool that retrieves SNP information from maf files from WXS
experiments"""


def main():
    # get command-line arguments
    args = parse_args(sys.argv[1:])

    # read the MAF table
    df = pd.DataFrame()
    for f in glob.glob(args.path[0] + "/*.maf"):
        current = read_maf_file(f, args.genes)
        df = df.append(current, ignore_index=True)

    df.to_csv(args.path[0] + "/merged.csv", index=False)


def read_maf_file(filepath, genes):
    """Read MAF file from GDC and build table in memory.
    :param: filepath Path to the MAF file
    :param: genes List of genes to filter by
    :return: Pandas DataFrame that has been appropriately filtered
    """
    df = pd.read_csv(filepath, sep='\t', comment='#')
    df = df.assign(Case=extract_case(filepath))
    gene_filtered = df[df["Hugo_Symbol"].isin(genes)]
    prop_filtered = gene_filtered[['Case', 'Hugo_Symbol', 'HGVSc',
                                   'HGVSp_Short', 'Chromosome',
                                   'Start_Position', 'Reference_Allele',
                                   'Tumor_Seq_Allele1', 'Tumor_Seq_Allele2',
                                   'dbSNP_RS', 't_depth', 't_ref_count',
                                   't_alt_count', 'n_depth']]
    return prop_filtered


def extract_case(filepath):
    """Pulls out the case name from a full filepath.
    Assumes files are formatted [case].wxs.aliquot_ensemble.masked.maf
    :param: filepath
    :return: Case name associated with file
    """
    base = os.path.basename(filepath)
    return base.split(".")[0]


def parse_args(arguments):
    """Parse the command line options.
    :return:  All script options
    """
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("path", type=str, nargs=1,
                        help="Path to directory containing MAFs")

    parser.add_argument("genes", type=str, nargs='+',
                        help='genes to search data for')

    args = parser.parse_args(arguments)
    if not args.path and not args.genes:
        parser.error("Path and genes required")

    return args


if __name__ == '__main__':
    main()
