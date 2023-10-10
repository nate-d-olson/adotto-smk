# Tandem Repeat Annotation Pipeline

[![Actions Status](https://github.com/mrvollger/SmkTemplate/workflows/CI/badge.svg)](https://github.com/mrvollger/SmkTemplate/actions)
[![Actions Status](https://github.com/mrvollger/SmkTemplate/workflows/Linting/badge.svg)](https://github.com/mrvollger/SmkTemplate/actions)
[![Actions Status](https://github.com/mrvollger/SmkTemplate/workflows/black/badge.svg)](https://github.com/mrvollger/SmkTemplate/actions)

This pipeline is designed to annotate tandem repeats in genomic sequences using various tools and custom scripts. It's built upon the Snakemake workflow management system.

## Background

The pipeline is based on the work found in the `regions` directory, where the methods used to develop the `adotto v1.0 GRCh38` tandem repeat database were developed and documented.
See the [adotto repo](https://github.com/ACEnglish/adotto/tree/main/regions) for additional information.

## Usage

To run the pipeline, you'll need Snakemake installed. Once you have it, you can initiate the pipeline using the following command:

```bash
snakemake --use-conda
```

This will execute the workflow, and Snakemake will automatically handle the creation of environments using Conda for each rule that requires specific software.

## Configuration

The pipeline requires a configuration file named `config.yaml` to specify various parameters and input data. The structure of this configuration file is as follows:

```yaml
references:
  GRCh37:
    REFURL: "URL_TO_GRCh37_REFERENCE"
    REF_MD5: "MD5_CHECKSUM_FOR_GRCh37"
    GIABTRURL: "URL_TO_GIAB_TR_STRATIFICATION_FOR_GRCh37"
    GIABTR_MD5: "MD5_CHECKSUM_FOR_GIAB_TR_FOR_GRCh37"
  GRCh38:
    REFURL: "URL_TO_GRCh38_REFERENCE"
    REF_MD5: "MD5_CHECKSUM_FOR_GRCh38"
    GIABTRURL: "URL_TO_GIAB_TR_STRATIFICATION_FOR_GRCh38"
    GIABTR_MD5: "MD5_CHECKSUM_FOR_GIAB_TR_FOR_GRCh38"
  CHM13:
    REFURL: "URL_TO_CHM13_REFERENCE"
    REF_MD5: "MD5_CHECKSUM_FOR_CHM13"
    GIABTRURL: "URL_TO_GIAB_TR_STRATIFICATION_FOR_CHM13"
    GIABTR_MD5: "MD5_CHECKSUM_FOR_GIAB_TR_FOR_CHM13"
n_splits: NUMBER_OF_SPLITS_FOR_FASTA
```

**Note:** Replace the placeholders (`URL_TO...`, `MD5_CHECKSUM_FOR...`, `NUMBER_OF_SPLITS_FOR_FASTA`) with the actual values as per your setup.

### Configuration Values

- `REFURL`: URL to the reference genome.
- `REF_MD5`: MD5 checksum for the reference genome to ensure data integrity.
- `GIABTRURL`: URL to the GIAB tandem repeat stratification data.
- `GIABTR_MD5`: MD5 checksum for the GIAB tandem repeat stratification data.
- `n_splits`: Specifies how many parts the reference genome should be split into during the RepeatMasker annotation phase.

---

## Contributing

If you'd like to contribute to the development of this pipeline or report any issues, please submit a pull request or raise an issue on the repository.
