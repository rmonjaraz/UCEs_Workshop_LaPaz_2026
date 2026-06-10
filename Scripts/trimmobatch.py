#!/usr/bin/env python3
__version__="v1.0"

"""
@author: Rodrigo Monjaraz-Ruedas (monroderik@gmail.com)

This is  a python wrapper for batch trimming of paired-end reads using Trimmomatic.

Configuration file is a CSV:
read_1.fastq.gz,read_2.fastq.gz,sample_name

"""

import argparse
import logging
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

#################################
# ADAPTERS
#################################

ADAPTER_FASTA = """>PrefixNX/1
AGATGTGTATAAGAGACAG
>PrefixNX/2
AGATGTGTATAAGAGACAG
>Trans1
TCGTCGGCAGCGTCAGATGTGTATAAGAGACAG
>Trans1_rc
CTGTCTCTTATACACATCTGACGCTGCCGACGA
>Trans2
GTCTCGTGGGCTCGGAGATGTGTATAAGAGACAG
>Trans2_rc
CTGTCTCTTATACACATCTCCGAGCCCACGAGAC
>PrefixPE/1
AATGATACGGCGACCACCGAGATCTACACTCTTTCCCTACACGACGCTCTTCCGATCT
>PrefixPE/2
CAAGCAGAAGACGGCATACGAGATCGGTCTCGGCATTCCTGCTGAACCGCTCTTCCGATCT
>PCR_Primer1
AATGATACGGCGACCACCGAGATCTACACTCTTTCCCTACACGACGCTCTTCCGATCT
>PCR_Primer1_rc
AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT
>PCR_Primer2
CAAGCAGAAGACGGCATACGAGATCGGTCTCGGCATTCCTGCTGAACCGCTCTTCCGATCT
>PCR_Primer2_rc
AGATCGGAAGAGCGGTTCAGCAGGAATGCCGAGACCGATCTCGTATGCCGTCTTCTGCTTG
>FlowCell1
TTTTTTTTTTAATGATACGGCGACCACCGAGATCTACAC
>FlowCell2
TTTTTTTTTTCAAGCAGAAGACGGCATACGA
>PrefixPE/1
TACACTCTTTCCCTACACGACGCTCTTCCGATCT
>PrefixPE/2
GTGACTGGAGTTCAGACGTGTGCTCTTCCGATCT
>PE1
TACACTCTTTCCCTACACGACGCTCTTCCGATCT
>PE1_rc
AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTA
>PE2
GTGACTGGAGTTCAGACGTGTGCTCTTCCGATCT
>PE2_rc
AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC
>PrefixPE/1
TACACTCTTTCCCTACACGACGCTCTTCCGATCT
>PrefixPE/2
GTGACTGGAGTTCAGACGTGTGCTCTTCCGATCT
"""

######################################
# CLI
######################################

def parse_args():

    parser = argparse.ArgumentParser(
        description="Batch trimming of paired-end reads using Trimmomatic"
    )

    parser.add_argument(
        "-I",
        "--input-list",
        required=True,
        help="CSV file containing: read1,read2,sample_name"
    )

    parser.add_argument(
        "-R",
        "--raw-reads",
        required=True,
        help="Directory containing raw FASTQ files"
    )

    parser.add_argument(
        "-O",
        "--output-prefix",
        required=True,
        help="Output prefix"
    )

    parser.add_argument(
        "-n",
        "--threads",
        type=int,
        default=6,
        help="Threads for Trimmomatic (default: 16)"
    )

    parser.add_argument(
        "-m",
        "--min-length",
        type=int,
        default=40,
        help="Minimum read length (default: 40)"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Reprocess samples even if outputs already exist"
    )

    parser.add_argument(
        '-v', '--version', 
        action='version', 
        version='%(prog)s ' + __version__
    )

    return parser.parse_args()

######################################
# LOGGING
######################################

def setup_logging(output_prefix):

    logfile = f"{output_prefix}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(logfile),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logging.info("Starting run")
    logging.info(f"Log file: {logfile}")

######################################
# READ IN SAMPLE LIST
######################################

def load_samples(input_file):
    samples = []
    with open(input_file) as fh:
        for line_number, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            fields = [x.strip() for x in line.split(",")]
            if len(fields) != 3:
                raise ValueError(
                    f"Line {line_number} does not contain 3 fields:\n{line}"
                )
            samples.append(
                {
                    "r1": fields[0],
                    "r2": fields[1],
                    "sample": fields[2]
                }
            )

    return samples

######################################
# CREATE TEMP ADAPTER FILE
######################################

def create_adapter_file():
    temp_adapter = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".fa",
        delete=False
    )

    temp_adapter.write(ADAPTER_FASTA)
    temp_adapter.close()

    return Path(temp_adapter.name)

######################################
# SINGLETON FILE
######################################

def create_singleton_file(read1_single, read2_single, singleton_out):
    with open(singleton_out, "wb") as outfile:
        for infile in [read1_single, read2_single]:
            with open(infile, "rb") as fh:
                shutil.copyfileobj(fh, outfile)

#####################################
# SAMPLE PROCESSING
#####################################

def process_sample(sample_info, raw_reads, output_root, adapter_file,
    threads, min_len, force):

    sample = sample_info["sample"]

    try:
        sample_dir = (
            output_root
            / sample
            / "split-adapter-quality-trimmed"
        )
        sample_dir.mkdir(
            parents=True,
            exist_ok=True
        )
        expected_output = (
            sample_dir /
            f"{sample}-READ1.fastq.gz"
        )
        if expected_output.exists() and not force:
            logging.info(
                f"Skipping {sample} (already completed)"
            )
            return (
                sample,
                "skipped",
                ""
            )

        r1_path = raw_reads / sample_info["r1"]
        r2_path = raw_reads / sample_info["r2"]

        if not r1_path.exists():
            raise FileNotFoundError(r1_path)

        if not r2_path.exists():
            raise FileNotFoundError(r2_path)

        logging.info(f"Processing {sample}")

        with tempfile.TemporaryDirectory(
            prefix=f"{sample}_"
        ) as tmpdir:

            tmpdir = Path(tmpdir)

            read1_out = tmpdir / f"{sample}-READ1.fastq.gz"
            read1_single = tmpdir / f"{sample}-READ1-single.fastq.gz"

            read2_out = tmpdir / f"{sample}-READ2.fastq.gz"
            read2_single = tmpdir / f"{sample}-READ2-single.fastq.gz"

            cmd = [
                "trimmomatic",
                "PE",
                "-threads",
                str(threads),

                str(r1_path),
                str(r2_path),

                str(read1_out),
                str(read1_single),

                str(read2_out),
                str(read2_single),

                f"ILLUMINACLIP:{adapter_file}:2:30:10",
                "LEADING:5",
                "TRAILING:15",
                "SLIDINGWINDOW:4:15",
                f"MINLEN:{min_len}"
            ]

            subprocess.run(
                cmd,
                check=True
            )

            singleton_out = (
                tmpdir /
                f"{sample}-READ-singleton.fastq.gz"
            )

            create_singleton_file(
                read1_single,
                read2_single,
                singleton_out
            )

            read1_single.unlink()
            read2_single.unlink()

            for file in tmpdir.glob("*.fastq.gz"):

                shutil.move(
                    str(file),
                    sample_dir / file.name
                )

        logging.info(f"Completed {sample}")

        return (
            sample,
            "success",
            ""
        )

    except Exception as e:

        logging.exception(
            f"Failed sample {sample}"
        )

        return (
            sample,
            "failed",
            str(e)
        )

#############################
# MAIN
#############################

def main():
    args = parse_args()
    setup_logging(args.output_prefix)
    raw_reads = Path(args.raw_reads).resolve()
    output_root = Path(
        f"{args.output_prefix}_clean_fastq"
    )
    output_root.mkdir(
        exist_ok=True
    )
    samples = load_samples(
        args.input_list
    )
    logging.info(
        f"Loaded {len(samples)} samples"
    )
    adapter_file = create_adapter_file()

    results = []

    try:

        for sample_info in samples:

            result = process_sample(
                sample_info=sample_info,
                raw_reads=raw_reads,
                output_root=output_root,
                adapter_file=adapter_file,
                threads=args.threads,
                min_len=args.min_length,
                force=args.force
            )

            results.append(result)

    finally:

        if adapter_file.exists():
            adapter_file.unlink()

    success = []
    failed = []
    skipped = []

    for sample, status, message in results:

        if status == "success":
            success.append(sample)

        elif status == "failed":
            failed.append((sample, message))

        elif status == "skipped":
            skipped.append(sample)

    logging.info("")
    logging.info("=" * 60)
    logging.info("RUN SUMMARY")
    logging.info("=" * 60)

    logging.info(
        f"Successful : {len(success)}"
    )

    logging.info(
        f"Skipped    : {len(skipped)}"
    )

    logging.info(
        f"Failed     : {len(failed)}"
    )

    if failed:

        logging.info("")
        logging.info("FAILED SAMPLES")

        for sample, error in failed:

            logging.info(
                f"{sample}: {error}"
            )

    logging.info("")
    logging.info("Finished")

    if failed:
        sys.exit(1)

    sys.exit(0)

############################

if __name__ == "__main__":
    main()
