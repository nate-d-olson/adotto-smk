import re
import sys
import pysam
from math import ceil


def chunk_into_n(lst, n):
    size = ceil(len(lst) / n)
    return list(map(lambda x: lst[x * size : x * size + size], list(range(n))))


if __name__ == "__main__":
    fasta_path = sys.argv[1]
    n_parts = int(sys.argv[2])
    output_dir = sys.argv[3]
    refid = sys.argv[4]

    f = pysam.FastaFile(fasta_path)
    for pos, i in enumerate(chunk_into_n(f.references, n_parts)):
        output_filename = f"{output_dir}/{refid}.part{pos}.fasta"
        with open(output_filename, "w") as fout:
            for ref in i:
                fout.write(f">{ref}\n")
                s = re.sub("(.{100})", "\\1\n", f[ref], 0, re.DOTALL).strip()
                fout.write(s + "\n")
