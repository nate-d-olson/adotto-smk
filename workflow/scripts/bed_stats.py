#!/usr/bin/env python3
"""
Make simple stats on a bed file - works inside a pipe so reads from stdin and writes the same to stdout
make a file with summary stats for span sizes
"""
import sys
import pandas as pd

spans = []
for line in sys.stdin:
    chrom, start, end = line.strip().split('\t')[:3]
    start = int(start)
    end = int(end)
    spans.append(abs(end - start))
    # sys.stdout.write(line)

spans = pd.Series(spans, name="span")
desc = spans.describe()

desc["tot_len"] = spans.sum()
desc = desc.dropna().astype(int).to_string()
sys.stdout.write(desc + '\n')