A subset of GRCh38 chr21 tandem repeat regions used for testing

The subset TR bed file was generated using the following
```
curl -L https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/genome-stratifications/v3.3/GRCh38@all/LowComplexity/GRCh38_AllTandemRepeats.bed.gz \
    > GRCh38_AllTandemRepeats.bed.gz
zcat GRCh38_AllTandemRepeats.bed.gz \
    | grep "^chr21" \
    | head -n 100 \
    > GRCh38chr21subset_AllTandemRepeats.bed
bgzip GRCh38chr21subset_AllTandemRepeats.bed
```
The resulting bed file was uploaded to aws.

A subset of GRCh38 chr21 was generated for use in tests and pipeline development
```
echo "chr21:1-5023000" | samtools faidx GRCh38_chr21.fasta.gz -r - > GRCh38chr21subset.fasta
## remove `:1-502300` from sequence name in fasta file
bgzip GRCh38chr21subset.fasta 
```