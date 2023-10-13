#!/usr/bin/env python3

"""
Script to parse the output of RepeatMasker and store the results in a Joblib file.
It focuses on entries with a RM_score greater than or equal to a specified threshold.

Usage:
    python repmask_to_joblib.py <output_file> <RM_output_files...>
"""

import joblib
import argparse
import logging
from truvari.annotations.repmask import RepMask
from collections import defaultdict


def parse_and_filter_repeatmasker(output_files, threshold):
    """
    Parses RepeatMasker output files and filters based on a score threshold.
    Returns the resulting data as a dictionary.
    """
    lookup = defaultdict(list)
    for file_path in output_files:
        data = RepMask.parse_output(file_path)
        for key in data:
            for item in data[key]:
                if item["RM_score"] >= threshold:
                    cls = item["RM_clsfam"].split("/")[0]
                    lookup[key].append((item["RM_score"], cls))
    return lookup


def main(args):
    logging.info("Parsing RepeatMasker output files...")
    lookup = parse_and_filter_repeatmasker(args.rm_output_files, args.threshold)
    joblib.dump(lookup, args.output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parse and filter RepeatMasker outputs, then save to Joblib."
    )
    parser.add_argument("output_file", help="Path for the output Joblib file.")
    parser.add_argument(
        "rm_output_files", nargs="+", help="RepeatMasker output files to parse."
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=225,
        help="Score threshold for filtering (default: 225).",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    main(args)
