#!/usr/bin/env python3
import os
import sys

def parse_fasta(fasta_path):
    """Parses a FASTA file and returns a dictionary of {header: sequence}."""
    sequences = {}
    current_header = None
    current_seq = []
    
    with open(fasta_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                if current_header:
                    sequences[current_header] = "".join(current_seq)
                # Extract first word as seqid to match GFF
                current_header = line[1:].split()[0]
                current_seq = []
            else:
                current_seq.append(line)
        if current_header:
            sequences[current_header] = "".join(current_seq)
            
    return sequences

def translate_codon(codon):
    """Translates a single codon to an amino acid using the standard genetic code."""
    codon_table = {
        'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
        'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
        'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
        'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
        'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
        'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
        'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
        'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
        'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
        'TAC':'Y', 'TAT':'Y', 'TAA':'*', 'TAG':'*',
        'TGC':'C', 'TGT':'C', 'TGA':'*', 'TGG':'W',
    }
    return codon_table.get(codon.upper(), 'X')

def translate_sequence(seq):
    """Translates a nucleotide sequence to protein sequence."""
    protein = []
    for i in range(0, len(seq), 3):
        codon = seq[i:i+3]
        if len(codon) == 3:
            protein.append(translate_codon(codon))
    return "".join(protein)

def parse_gff_attributes(attr_str):
    """Parses GFF3 attribute column into a dictionary."""
    attributes = {}
    for item in attr_str.split(';'):
        if '=' in item:
            key, val = item.split('=', 1)
            attributes[key.strip()] = val.strip()
    return attributes

def main():
    fasta_path = 'genome.fa'
    gff_path = 'annotations.gff3'
    
    if not os.path.exists(fasta_path) or not os.path.exists(gff_path):
        # Try relative paths
        trap_path = os.path.join('..', '..', 'exercises', 'week2', 'trap')
        if os.path.exists(os.path.join(trap_path, fasta_path)):
            fasta_path = os.path.join(trap_path, fasta_path)
            gff_path = os.path.join(trap_path, gff_path)
        else:
            print(f"Error: {fasta_path} or {gff_path} not found in current directory.", file=sys.stderr)
            sys.exit(1)
            
    # Load genome sequence
    genome = parse_fasta(fasta_path)
    
    # Process GFF3 file
    with open(gff_path, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split('\t')
            if len(parts) < 9:
                continue
                
            seqid, source, feature_type, start_str, end_str, score, strand, phase, attributes_str = parts
            
            if feature_type != 'CDS':
                continue
                
            start = int(start_str)
            end = int(end_str)
            
            # Retrieve sequence of the chromosome
            if seqid not in genome:
                print(f"Warning: Chromosome {seqid} not found in genome FASTA.", file=sys.stderr)
                continue
                
            chr_seq = genome[seqid]
            
            # GFF coordinates are 1-based, inclusive.
            # Python slice is 0-based, end-exclusive.
            # Therefore, GFF [start, end] corresponds to Python slice [start-1:end].
            cds_seq = chr_seq[start - 1 : end]
            
            # Handle reverse strand if necessary (though the input sample is + strand, let's be robust)
            if strand == '-':
                # Reverse complement
                complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'N': 'N',
                              'a': 't', 't': 'a', 'c': 'g', 'g': 'c', 'n': 'n'}
                cds_seq = "".join(complement.get(base, base) for base in reversed(cds_seq))
            
            # Translate to protein
            protein_seq = translate_sequence(cds_seq)
            
            # Parse attributes to get gene name
            attrs = parse_gff_attributes(attributes_str)
            gene_name = attrs.get('Name', attrs.get('ID', 'unknown_gene'))
            
            # Print gene_name <TAB> nt_sequence <TAB> protein_sequence
            print(f"{gene_name}\t{cds_seq}\t{protein_seq}")

if __name__ == '__main__':
    main()
