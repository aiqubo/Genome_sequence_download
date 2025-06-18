import csv
import re
import os
import sys
import getopt
import urllib.parse
import time
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("download.log", mode='w'),
        logging.StreamHandler()
    ]
)

GenomeList = None
OutDir = "./"
MaxRetries = 3

def create_directories():
    try:
        Path(OutDir).mkdir(parents=True, exist_ok=True)
        Path(f"{OutDir}/out").mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create directories: {e}")
        sys.exit(1)

def validate_file(file_path):
    if not os.path.isfile(file_path):
        logging.error(f"File does not exist: {file_path}")
        return False
    if not os.access(file_path, os.R_OK):
        logging.error(f"File is not readable: {file_path}")
        return False
    return True

def download_file(url, output_dir, retries=MaxRetries):
    safe_url = urllib.parse.quote(url, safe=':/')
    file_name = os.path.basename(url)
    output_path = os.path.join(output_dir, file_name)
    
    if os.path.exists(output_path):
        logging.info(f"Skipping download, file exists: {file_name}")
        return True
    
    for attempt in range(retries):
        try:
            cmd = f"aria2c -x 16 {safe_url} -d {output_dir}"
            logging.info(f"Download attempt ({attempt+1}/{retries}): {file_name}")
            status = os.system(cmd)
            
            if status == 0:
                logging.info(f"Download successful: {file_name}")
                return True
            else:
                logging.warning(f"Download failed ({attempt+1}/{retries}): {file_name}")
                time.sleep(2 ** attempt)
            
        except Exception as e:
            logging.error(f"Exception during download: {e}")
            time.sleep(2 ** attempt)
    
    logging.error(f"Download failed after max retries: {file_name}")
    return False

def main():
    global GenomeList, OutDir
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:l:o:", ["help", "GenomeList=", "OutDir="])
    except getopt.GetoptError as err:
        logging.error(f"Parameter parsing error: {err}")
        print_usage()
        sys.exit(2)
    
    for name, value in opts:
        if name in ("-h", "--help"):
            print_usage()
            sys.exit(0)
        elif name in ("-l", "--GenomeList"):
            GenomeList = value
        elif name in ("-o", "--OutDir"):
            OutDir = value
    
    if GenomeList is None:
        logging.error("Error: Genome list file is required (-l or --GenomeList)")
        print_usage()
        sys.exit(2)
    
    create_directories()
    
    if not validate_file(GenomeList):
        sys.exit(1)
    
    try:
        success_count = 0
        fail_count = 0
        
        with open(GenomeList, "r") as f:
            csv_reader = csv.reader(f, delimiter="\t")
            next(csv_reader, None)
            
            for row_num, row in enumerate(csv_reader, start=2):
                if not row or not row[0]:
                    continue
                
                try:
                    gcf_part = row[0]
                    assembly_name = row[1] if len(row) > 1 else "unknown"
                    
                    url = (f"https://ftp.ncbi.nlm.nih.gov/genomes/all/{gcf_part[:3]}/"
                           f"{gcf_part[4:7]}/{gcf_part[7:10]}/{gcf_part[10:13]}/"
                           f"{gcf_part}_{assembly_name}/{gcf_part}_{assembly_name}_genomic.fna.gz")
                    
                    success = download_file(url, f"{OutDir}/out")
                    
                    if success:
                        success_count += 1
                    else:
                        fail_count += 1
                
                except Exception as e:
                    fail_count += 1
                    logging.error(f"Error processing row {row_num}: {e}")
        
        logging.info(f"Download completed. Success: {success_count}, Failed: {fail_count}")
    
    except Exception as e:
        logging.error(f"Critical error: {e}")
        sys.exit(1)

def print_usage():
    print('''
Usage: python download_genomes.py [options]

Options:
  -h, --help            Show this help message and exit
  -l, --GenomeList      Specify genome list file path (required)
  -o, --OutDir          Specify output directory (default: ./)
''')

if __name__ == "__main__":
    main()
