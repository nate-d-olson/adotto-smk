#!/usr/bin/env python3

"""
Script to combine genomic regions and their annotations into a structured format.
The script outputs data in a format where each line consists of a genomic region 
and its associated annotations in JSON format.

Usage:
    python tr_reganno_maker.py <regions_file> <annotations_file>
"""

import json
import tabix
import truvari
import argparse
import logging


def main(reg_fn, anno_fn):
    """
    Combine regions and annotations into a file.
    """
    header = [
        ("chrom", str),
        ("start", int),
        ("end", int),
        ("period", float),
        ("copies", float),
        ("score", int),
        ("entropy", float),
        ("repeat", str),
    ]

    tb = tabix.open(anno_fn)
    for line in truvari.opt_gz_open(reg_fn):
        chrom, start, end = line.strip().split("\t")[:3]
        start = int(start)
        end = int(end)
        m_data = []
        for i in tb.query(chrom, start, end):
            try:
                m_data.append({fmt[0]: fmt[1](x) for x, fmt in zip(i, header)})
            except tabix.TabixError as e:
                logging.warning(
                    f"Tabix error for region {chrom}:{start}-{end}. Error message: {e}"
                )
                pass
        data_str = json.dumps(m_data)
        print(f"{chrom}\t{start}\t{end}\t{data_str}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Combine genomic regions and their annotations."
    )
    parser.add_argument("regions_file", help="Path to the regions file.")
    parser.add_argument("annotations_file", help="Path to the annotations file.")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    main(args.regions_file, args.annotations_file)
