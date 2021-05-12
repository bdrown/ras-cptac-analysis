##################################################################
# rename-files.py
# Reads samples sheets and then renames files downloaded from GDC
# data portal.
#
# Author: Bryon Drown (Northwestern University)
# Created: May 7, 2021
#
# Usage: python rename-files.py [Path to samplesheet] [Directory]
# Outcome: renames the files in the provided directory according
#   to the contents of the provided sample sheet
##################################################################

import argparse
import sys
import os
import pandas as pd

__doc__ = """Tool that renames files according to the tissue
sample identifier"""


def main():
    # get command-line arguments
    args = parse_args(sys.argv[1:])

    # figure out what should be renamed to what
    samples = read_sample_list(args.sample_info[0])

    # perform the renaming
    rename_samples(samples, args.path[0])


def read_sample_list(filename):
    # read the sample sheet
    df = pd.read_csv(filename, delimiter="\t")

    # check if the Case ID is a single entry or is separated by commas
    if "," in df['Case ID'][1]:
        # if there are multiple case IDs listed, just take the first one
        df['Case ID'] = df['Case ID'].str.split(", ", n=1, expand=True)

    # generate new filenames. steps:
    # 1. remove .gz from old name
    if ".gz" in df['File Name'][1]:
        df['File Name'] = df['File Name'].str.rpartition('.')[0]

    # 2. copy old to new
    # 3. remove first element
    df['New Name'] = df['File Name'].str.partition('.')[2]

    # 4. prepend case ID
    df['New Name'] = df['Case ID'] + '.' + df['New Name']

    return df


def rename_samples(samples, path):
    for index, row in samples.iterrows():
        # filenames should be appropriate for OS
        src = os.path.join(path, row['File Name'])
        dst = os.path.join(path, row['New Name'])

        # logging
        print("Renaming " + src + " to " + dst)

        # system call
        os.rename(src, dst)


def parse_args(arguments):
    """Parse the command line options.
    :return:  All script options
    """
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("sample_info", type=str, nargs=1,
                        help="Path to sample sheet")

    parser.add_argument("path", type=str, nargs=1,
                        help="Path to directory containing MAFs")

    args = parser.parse_args(arguments)
    if not args.path or not args.sample_info:
        parser.error("Sample sheet and path to directory required")

    return args


if __name__ == '__main__':
    main()
