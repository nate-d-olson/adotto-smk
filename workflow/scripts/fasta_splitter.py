#!/usr/bin/env python3

"""
Splitter for Fasta Files by Sequences

This script takes a fasta file and divides it into smaller parts based on the number of sequences.
Each part will contain an approximately equal number of sequences. The script will output separate
fasta files for each part. Script based on code by AC English, https://github.com/ACEnglish/adotto/blob/main/regions/scripts/fasta_splitter.py

Usage:
    ./fasta_splitter.py --fasta_path <path_to_fasta> --n_parts <number_of_parts> 
                        --output_dir <output_directory> --refid <reference_id>

Author: ND Olson
Date: 2023-10-10
Version: 1.0
"""

import re
import sys
import pysam
import argparse
import logging
from math import ceil


def chunk_into_n(lst, n):
    """
    Divide a list into approximately equal parts.

    Parameters:
    - lst (list): The list to be divided.
    - n (int): The number of parts.

    Returns:
    - list of lists: A list containing sublists of approximately equal sizes.
    """
    size = ceil(len(lst) / n)
    return list(map(lambda x: lst[x * size : x * size + size], list(range(n))))


def main(args):
    """
    Main function to execute the fasta splitting process.

    Parameters:
    - args (argparse.Namespace): Parsed command-line arguments.
    """
    f = pysam.FastaFile(args.fasta_path)

    # Assert that the number of parts is not greater than the number of sequences
    num_sequences = len(f.references)
    assert args.n_parts <= num_sequences, (
        f"The input fasta file has {num_sequences} sequences. "
        f"The number of parts ({args.n_parts}) cannot be greater than that number."
    )

    for pos, i in enumerate(chunk_into_n(f.references, args.n_parts)):
        output_filename = f"{args.output_dir}/{args.refid}.part{pos}.fasta"
        with open(output_filename, "w") as fout:
            for ref in i:
                fout.write(f">{ref}\n")
                s = re.sub("(.{100})", "\\1\n", f[ref], 0, re.DOTALL).strip()
                fout.write(s + "\n")
        logging.info(f"Written {output_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split fasta file by sequences.")
    parser.add_argument(
        "--fasta_path", required=True, help="Path to the input fasta file."
    )
    parser.add_argument(
        "--n_parts",
        type=int,
        required=True,
        help="Number of parts to split the fasta into.",
    )
    parser.add_argument(
        "--output_dir", required=True, help="Directory to save the split fasta files."
    )
    parser.add_argument(
        "--refid", required=True, help="Reference ID for naming the split fasta files."
    )
    parser.add_argument(
        "--log_level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level",
    )

    args = parser.parse_args()

    # Setting up logging
    logging.basicConfig(
        level=args.log_level, format="%(asctime)s [%(levelname)s] - %(message)s"
    )

    main(args)
