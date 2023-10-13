#!/usr/bin/env python3

"""
Make simple stats on a BED file.
The script reads a BED file from stdin, computes the span for each entry, 
and then prints summary statistics to stdout.
Expected Input: BED format data from stdin
Output: Descriptive statistics of span sizes printed to stdout
"""

import sys
import pandas as pd


def compute_spans_from_bed(input_stream):
    spans = []
    for line in input_stream:
        try:
            chrom, start, end = line.strip().split("\t")[:3]
            start = int(start)
            end = int(end)
            spans.append(end - start)
        except ValueError:
            sys.stderr.write(f"Warning: Malformed BED line encountered: {line}")
    return spans


def main():
    spans = compute_spans_from_bed(sys.stdin)
    spans_series = pd.Series(spans, name="span")
    desc = spans_series.describe()
    desc["tot_len"] = spans_series.sum()
    desc = desc.dropna().astype(int).to_string()
    sys.stdout.write(desc + "\n")


if __name__ == "__main__":
    main()
