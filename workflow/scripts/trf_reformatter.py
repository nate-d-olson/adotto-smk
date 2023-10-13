#!/usr/bin/env python3
"""
Script to parse the output of Tandem Repeat Finder (TRF) and transform it into a structured format.
The script translates the coordinates based on the 'samtools faidx' fetched sequence header 
back to whole-genome coordinates. The processed data is saved as a compressed Joblib file and a tab-separated file.

Usage:
    python trf_reformatter.py <TRF_output_path> <output_name>

Notes:
samtools faidx is 1-based

The bedfiles are (presumably) 0 based
And so are trf output is 0-based, I think.

0-based index - fetched 1-based region so I should add 1 to the starts when parsing the header

this is complex. Let's just take the header and add the start/end to the header start position to translate it
Then  I can do some pysam.FastaFile.fetch to check that the coordinates are right

## Script developed by AC English and copied from https://github.com/ACEnglish/adotto/blob/main/regions/scripts/trf_reformatter.py
"""
import sys
import joblib
import pandas as pd
import argparse


def parse_trf_output(tr_fn):
    """
    Parses the output from Tandem Repeat Finder (TRF) and returns a DataFrame.
    Translates the coordinates based on the 'samtools faidx' fetched sequence header back to whole-genome coordinates.
    """
    trf_cols = [
        ("start", int),
        ("end", int),
        ("period", int),
        ("copies", float),
        ("consize", int),
        ("pctmat", int),
        ("pctindel", int),
        ("score", int),
        ("A", int),
        ("C", int),
        ("G", int),
        ("T", int),
        ("entropy", float),
        ("repeat", str),
        ("upflank", str),
        ("sequence", str),
        ("dnflank", str),
    ]

    data_entries = []

    with open(tr_fn, "r") as fh:
        while True:
            line = fh.readline()
            if not line:
                break

            if line.startswith("@"):
                name = line.strip()[1:]
                chrom, coords = name.split(":")
                wgs_start, wgs_end = map(int, coords.split("-"))
                wgs_start -= 2
                continue

            line_data = line.strip().split(" ")
            data = {
                x[0]: x[1](y) for x, y in zip(trf_cols, line_data) if x[1] is not None
            }
            data["chrom"] = chrom
            data["in_region_start"] = wgs_start
            data["in_region_end"] = wgs_end
            data["start"] += wgs_start
            data["end"] += wgs_start
            data_entries.append(data)

    return pd.DataFrame(data_entries)


def main(args):
    data = parse_trf_output(args.trf_output_path)
    joblib.dump(data, args.output_name + ".jl", compress=5)
    columns = [
        "chrom",
        "start",
        "end",
        "period",
        "copies",
        "score",
        "entropy",
        "repeat",
    ]
    data[columns].to_csv(args.output_name, sep="\t", index=False, header=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse and reformat TRF output.")
    parser.add_argument("trf_output_path", help="Path to the TRF output file.")
    parser.add_argument("output_name", help="Base name for the output files.")
    args = parser.parse_args()

    main(args)
