#!/usr/bin/env python3

"""
Filter regions from a BED file based on certain criteria:
- Removes regions outside of known chromosomes.
- Removes regions where the end position is less than or equal to the start position.
- Removes regions with spans (end - start) less than 10.
- Removes regions with spans greater than 50,000.

The script reads a BED file from stdin and prints the retained regions to stdout.
It also writes a summary of the filtering to stderr and a detailed JSON summary to a specified file.

Usage:
    cat input.bed | python filter_tr_regions.py [output.json]
"""

import sys
import json
import argparse


def filter_regions(input_stream, output_json):
    known_chrs = (
        [f"chr{n}" for n in range(1, 23)]
        + ["chrY", "chrX", "X", "Y"]
        + [str(n) for n in range(1, 23)]
    )
    tot_cnt, chr_rm_cnt, sm_rm_cnt, big_rm_cnt, flip_rm_cnt, span_rm, span_kept = (
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    )

    for line in input_stream:
        tot_cnt += 1
        chrom, start, end = line.strip().split("\t")
        start, end = int(start), int(end)
        span = abs(end - start)

        if chrom not in known_chrs:
            chr_rm_cnt += 1
            span_rm += span
            continue
        if end <= start:
            flip_rm_cnt += 1
            span_rm += span
            continue
        if span < 10:
            sm_rm_cnt += 1
            span_rm += span
            continue
        if span > 50000:
            big_rm_cnt += 1
            span_rm += span
            continue

        span_kept += span
        print(f"{chrom}\t{start}\t{end}")

    span_total = span_kept + span_rm
    span_pct = span_rm / span_total * 100
    rm_cnt = sm_rm_cnt + big_rm_cnt + flip_rm_cnt + chr_rm_cnt
    pct_rm = rm_cnt / tot_cnt * 100

    sys.stderr.write(
        f"""
Count removed {rm_cnt} of {tot_cnt} = {tot_cnt - rm_cnt} ({pct_rm:.2f}%)
Span removed {span_rm} of {span_total} = {span_kept} ({span_pct:.2f}%)
Chromosome removed: {chr_rm_cnt}
Small removed: {sm_rm_cnt}
Big removed: {big_rm_cnt}
Coord remove: {flip_rm_cnt}
"""
    )

    stats = {
        "total": tot_cnt,
        "removed": rm_cnt,
        "removed_pct": pct_rm,
        "chrom_rm": chr_rm_cnt,
        "small_rm": sm_rm_cnt,
        "big_rm": big_rm_cnt,
        "coord_rm": flip_rm_cnt,
        "span_total": span_total,
        "span_rm": span_rm,
        "span_kept": span_kept,
    }

    with open(output_json, "w") as f:
        json.dump(stats, f, indent=4)


def main():
    parser = argparse.ArgumentParser(description="Filter regions from a BED file.")
    parser.add_argument("output_json", help="Path to the output JSON summary file.")
    args = parser.parse_args()

    filter_regions(sys.stdin, args.output_json)


if __name__ == "__main__":
    main()
