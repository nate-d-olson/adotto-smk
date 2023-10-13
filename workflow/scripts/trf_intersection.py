#!/usr/bin/env python3

"""
Script to compute the intersections between the initial bed file with tandem repeat regions and
a bed file generated by parsing the output after annotating the bed file with trf.
The script utilizes bedtools for performing intersections and saves the results in a compressed Joblib file.

Usage:
    python trf_intersection.py <regions_bed> <trf_bed> <intersection_jl>

Code modified from an inital script developed by AC English 
https://github.com/ACEnglish/adotto/blob/main/regions/scripts/bed_intersection_stats.py
"""

import re
import joblib
import logging
import truvari
import pandas as pd
import argparse


def do_intersection(a, b, ro=None):
    """
    Intersects two given BED files using bedtools.
    Processes the output to count the intersections and returns this data as a pandas DataFrame.
    """
    cmd_tmpl = "bedtools intersect -a {a} -b {b} -c {ro}"
    cmd_tmpl += "| cut -f4 | sort -n | uniq -c"
    if ro:
        ro = f"-r -f 0.50"
    else:
        ro = ""
    cmd = cmd_tmpl.format(a=a, b=b, ro=ro)
    ret = truvari.cmd_exe(cmd)
    data = []
    for line in ret.stdout.strip().split("\n"):
        row = re.split("\\s+", line.strip())
        data.append(row)
    data = pd.DataFrame(data, columns=["count", "intersection"])
    data = data.astype(int)
    return data


def main(args):
    truvari.setup_logging()
    logging.info("Intersecting BED files %s and %s", args.regions_bed, args.trf_bed)
    data = do_intersection(args.bregions_bed, args.trf_bed, ro=False)
    data["ro"] = False
    joblib.dump(data, args.intersection_jl)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Intersection of initial bed file and bed file with trf annotations."
    )
    parser.add_argument("regions_bed", help="Path to the initial regions bed.")
    parser.add_argument("trf_bed", help="Path to trf annotations bed.")
    parser.add_argument("intersection_jl", help="Path for the output Joblib file.")
    args = parser.parse_args()

    main(args)