#!/usr/bin/env python3
"""Calculate allele frequencies per chromosome from a VCF file.

This script parses a VCF file (plain text or gzipped), extracts allele frequencies,
and outputs the summary statistics (mean, median, count) per chromosome. It can calculate
frequencies either from the INFO/AF field or by directly parsing sample genotypes (GT).
"""

import argparse
import collections
import gzip
import sys
from pathlib import Path


def parse_vcf(vcf_path):
    """Parses a VCF file and yields chromosome, info dict, and genotypes list."""
    open_func = gzip.open if str(vcf_path).endswith(".gz") else open
    mode = "rt" if str(vcf_path).endswith(".gz") else "r"

    try:
        with open_func(vcf_path, mode, encoding="utf-8") as f:
            for line in f:
                if line.startswith("#"):
                    continue
                parts = line.strip().split("\t")
                if len(parts) < 8:
                    continue
                chrom = parts[0]
                info_raw = parts[7]
                
                # Parse INFO field into key-value pairs
                info = {}
                for item in info_raw.split(";"):
                    if "=" in item:
                        key, val = item.split("=", 1)
                        info[key] = val
                    else:
                        info[item] = True

                # Parse sample genotypes if present
                genotypes = []
                if len(parts) > 9:
                    format_field = parts[8].split(":")
                    try:
                        gt_idx = format_field.index("GT")
                        for sample in parts[9:]:
                            sample_fields = sample.split(":")
                            if gt_idx < len(sample_fields):
                                gt = sample_fields[gt_idx]
                                # GT can be e.g. 0/1, 0|1, 1/2, ./., etc.
                                genotypes.append(gt)
                    except ValueError:
                        pass # GT not in FORMAT

                yield chrom, info, genotypes
    except FileNotFoundError:
        print(f"Error: File '{vcf_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading VCF file: {e}", file=sys.stderr)
        sys.exit(1)


def calculate_frequencies(vcf_path):
    """Aggregates allele frequencies per chromosome."""
    # We will track allele frequencies computed from INFO/AF and GT
    chrom_info_af = collections.defaultdict(list)
    chrom_gt_af = collections.defaultdict(list)

    for chrom, info, genotypes in parse_vcf(vcf_path):
        # 1. From INFO field (AF tag)
        if "AF" in info:
            try:
                # AF can be comma-separated for multi-allelic sites
                afs = [float(x) for x in str(info["AF"]).split(",")]
                chrom_info_af[chrom].extend(afs)
            except ValueError:
                pass

        # 2. From genotypes
        if genotypes:
            total_alleles = 0
            alt_alleles = 0
            for gt in genotypes:
                # Clean up phase symbols and split alleles
                gt_clean = gt.replace("|", "/").split("/")
                for allele in gt_clean:
                    if allele == ".":
                        continue
                    try:
                        allele_idx = int(allele)
                        total_alleles += 1
                        if allele_idx > 0:
                            alt_alleles += 1
                    except ValueError:
                        pass
            if total_alleles > 0:
                chrom_gt_af[chrom].append(alt_alleles / total_alleles)

    return chrom_info_af, chrom_gt_af


def print_summary(chrom_info_af, chrom_gt_af):
    """Prints a beautiful markdown table summarizing the allele frequencies."""
    all_chroms = sorted(list(set(chrom_info_af.keys()) | set(chrom_gt_af.keys())))

    if not all_chroms:
        print("No variant data found in the VCF file.")
        return

    print(f"{'Chromosome':<12} | {'Source':<10} | {'Variants':<10} | {'Mean AF':<10} | {'Median AF':<10}")
    print("-" * 62)

    for chrom in all_chroms:
        # Print info from INFO field if available
        if chrom in chrom_info_af and chrom_info_af[chrom]:
            afs = sorted(chrom_info_af[chrom])
            count = len(afs)
            mean_af = sum(afs) / count
            median_af = afs[count // 2]
            print(f"{chrom:<12} | {'INFO/AF':<10} | {count:<10} | {mean_af:<10.4f} | {median_af:<10.4f}")

        # Print info from Genotypes if available
        if chrom in chrom_gt_af and chrom_gt_af[chrom]:
            afs = sorted(chrom_gt_af[chrom])
            count = len(afs)
            mean_af = sum(afs) / count
            median_af = afs[count // 2]
            print(f"{chrom:<12} | {'Sample GT':<10} | {count:<10} | {mean_af:<10.4f} | {median_af:<10.4f}")


def generate_mock_vcf(path):
    """Generates a sample VCF file for testing purposes."""
    content = """##fileformat=VCFv4.2
##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSample1\tSample2\tSample3
chr1\t1001\t.\tA\tG\t100\tPASS\tAF=0.25\tGT\t0/0\t0/1\t0/0
chr1\t1050\t.\tT\tC\t100\tPASS\tAF=0.50\tGT\t0/1\t0/1\t1/0
chr2\t2001\t.\tC\tG\t100\tPASS\tAF=0.75\tGT\t1/1\t0/1\t1/1
chr2\t2100\t.\tG\tA\t100\tPASS\tAF=0.10\tGT\t0/0\t0/0\t0/1
chrX\t5001\t.\tA\tT\t100\tPASS\tAF=1.00\tGT\t1/1\t1/1\t1/1
"""
    Path(path).write_text(content, encoding="utf-8")
    print(f"Generated mock VCF file at: {path}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Calculate allele frequencies per chromosome from a VCF file."
    )
    parser.add_argument("vcf_file", nargs="?", help="Path to the input VCF file (.vcf or .vcf.gz)")
    parser.add_argument(
        "--mock", action="store_true", help="Generate a mock VCF file (mock.vcf) and run the script on it."
    )

    args = parser.parse_args()

    if args.mock:
        mock_path = "mock.vcf"
        generate_mock_vcf(mock_path)
        chrom_info_af, chrom_gt_af = calculate_frequencies(mock_path)
        print_summary(chrom_info_af, chrom_gt_af)
        return

    if not args.vcf_file:
        parser.print_help()
        print("\nError: Please provide a VCF file path or use --mock.", file=sys.stderr)
        sys.exit(1)

    chrom_info_af, chrom_gt_af = calculate_frequencies(args.vcf_file)
    print_summary(chrom_info_af, chrom_gt_af)


if __name__ == "__main__":
    main()
