# Genome Downloader

## Overview
The Genome Downloader is a Python script designed to download genomic data from the NCBI FTP server. It processes a tabular list of genomes, generates download URLs, and uses aria2c for efficient parallel downloads with retry capabilities.

## Installation Requirements:
Python 3.9+
Parallel Downloads: Utilizes aria2c to download files with 16 connections per file
```
git clone https://github.com/your-repo/genome-downloader.git
cd genome-downloader
```
## TSV file prepare
[NCBI Genome](https://www.ncbi.nlm.nih.gov/datasets/genome/) Download --> Download Table\
### As follow:
![image](https://github.com/user-attachments/assets/0d5e1b72-dfbb-480e-886b-99de4b8752ca)


## Usage:

python sequence_download.py [--help] [--version] [--fasta FASTA] [--length LENGTH] [--nomask] [--param PARAM] [--output OUTPUT]

**example:**
```
python sequence_download.py --GenomeList /path/to/genome_list.tsv
```

**optional arguments:**
| Arguments      | Note |
| -------------  | ----------------------------------------------------------------------------------------------|
| -h, --help     |#show this help message and exit                                                               |
|--GenomeList    |#Specify genome list file path (required)                                                      |
|  --OutDir      |#Specify output directory (default: ./)                                                        |

## Cite
[Genome Downloader](https://github.com/aiqubo/Genome_sequence_download)
