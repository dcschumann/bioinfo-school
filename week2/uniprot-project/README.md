# UniProt Summary Table

Queries the UniProt REST API for a list of protein IDs and outputs
a TSV summary table with protein length, organism, and domain annotations.

## Inputs
- `uniprot_ids.txt` — plain text file, one UniProt ID per line

Example:
P69905
P68871
P00533
P04637
Q9Y233

## Outputs
- `uniprot_summary.tsv` — tab-separated table with columns:
  UniProt ID | Protein Length | Organism | Domain Annotations

## Dependencies
Python 3.x and the following package:

pip install requests

## How to run
python uniprot_summary.py uniprot_ids.txt uniprot_summary.tsv

## Known issues
- urllib.parse is imported but not used — can be removed safely
- No rate limiting between requests — add time.sleep(0.5) if querying large ID lists
- Domain annotations show "None" for proteins with no Pfam-style domain features in UniProt (e.g. p53/P04637) — this is correct behaviour, not a bug

## Validation
After running, check:
- P68871 (haemoglobin beta) should have length 147
- P04637 (p53) should have organism Homo sapiens
- No empty fields for known IDs