import re
import sys
import joblib
import logging
import truvari
import pandas as pd


def do_intersection(a, b, ro=None):
    """
    Returns the intersection counts as a dataframe
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
        row = re.split("\s+", line.strip())
        data.append(row)
    data = pd.DataFrame(data, columns=["count", "intersection"])
    data = data.astype(int)
    return data


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python bed_intersection_single_source.py <path_to_merged_bed>")
        sys.exit(1)

    merged_bed_path = sys.argv[1]
    tr_bed = "data/tr_annotated.bed.gz"
    source = merged_bed_path.split("/")[
        -2
    ]  # Extracting source name from the directory name
    truvari.setup_logging()
    logging.info("intersecting %s", source)
    dat = do_intersection(merged_bed_path, tr_bed, ro=False)
    dat["source"] = source
    dat["ro"] = False
    dat_ro = do_intersection(merged_bed_path, tr_bed, ro=True)
    dat_ro["source"] = source
    dat_ro["ro"] = True
    data = pd.concat([dat, dat_ro])
    joblib.dump(data, "results/intersection.jl")
