"""Small FASTA summarizer for Week 2 (Fixed).

The behavior is: read a FASTA file, print one row per sequence, and report sequence
length plus GC percentage.
"""

from pathlib import Path


def read_fasta(path):
    records = {}
    current_name = None
    current_seq = []

    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if line.startswith(">"):
            if current_name:
                records[current_name] = "".join(current_seq)
            current_name = line[1:]
            current_seq = []
        else:
            current_seq.append(line)

    if current_name:
        records[current_name] = "".join(current_seq)

    return records


def gc_percent(sequence):
    if not sequence:
        return 0.0
    sequence = sequence.upper()
    gc = sequence.count("G") + sequence.count("C")
    return gc / len(sequence)


def main():
    # Resolve example.fa relative to the script's position
    script_dir = Path(__file__).parent
    # Path to example.fa in exercises/week2/
    fasta_path = script_dir / "../../exercises/week2/example.fa"
    records = read_fasta(fasta_path.resolve())

    for name, sequence in records.items():
        print(name, len(sequence), gc_percent(sequence))


if __name__ == "__main__":
    main()
