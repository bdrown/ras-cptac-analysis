##################################################################
# de-isoforms
# Compares the differential expression of RAS isoforms across samples
# Author: Bryon Drown (Northwestern University)
# Created: June 1, 2021
#
# Usage: python de-isoforms.py [Directory with Salmon output] [Genes to search]
# Generates: merged.csv file
##################################################################

import argparse
import sys
import os
import pandas as pd
import glob
import re

__doc__ = """Tool that retrieves differential expression information
from CPTAC data"""

def main():
    # get command-line arguments
    args = parse_args(sys.argv[1:])

    # read the genes of interest
    genes = pd.read_csv(args.genes, sep='\t')

    # read through the Salmon quant
    df = pd.DataFrame()
    for f in glob.glob(args.path[0] + "/**/quant.sf", recursive=True):
        current = read_salmon_output(f, genes)
        df = df.append(current, ignore_index=True)

    df.to_csv(args.path[0] + "/merged.csv", index=False)

# TODO rework method for salmon output
def read_salmon_output(filepath, genes):
    """Read fpkm file from GDC and build table in memory.
    :param: filepath Path to the salmon quant file
    :param: genes List of genes to filter by
    :return: Pandas DataFrame that has been appropriately filtered
    """
    df = pd.read_csv(filepath, sep='\t')
    df = df.assign(Case=extract_case(filepath))
    gene_filtered = df[df["Name"].isin(genes)]
    return gene_filtered


def extract_case(filepath):
    """Pulls out the case name from a full filepath.
    Assumes files are formatted salmon/[case]/quant.sf
    :param: filepath
    :return: Case name associated with file
    """
    pat = re.compile('\/(\d{2}CO\d{3})\/quant.sf')
    base = pat.findall(filepath)
    if len(base) > 0:
        return base[0]
    else:
        return 'Unknown Case'

def parse_args(arguments):
    """Parse the command line options.
    :return:  All script options
    """
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("path", type=str, nargs=1,
                        help="Path to directory containing Salmon output folders")

    parser.add_argument("gene_list", type=str, nargs=1,
                        help='TSV file that lists transcripts of interest')

    args = parser.parse_args(arguments)
    if not args.path and not args.genes:
        parser.error("Path and genes required")

    return args


if __name__ == '__main__':
    main()
