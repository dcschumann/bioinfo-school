import os
import sys
import argparse
import requests
import urllib.parse

def fetch_uniprot_info(uniprot_id):
    """
    Fetch protein length, organism, and domain annotations for a UniProt ID
    using the UniProt KB REST API (JSON).
    """
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 404:
            print(f"Warning: UniProt ID {uniprot_id} not found (404).", file=sys.stderr)
            return None
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {uniprot_id}: {e}", file=sys.stderr)
        return None

    # 1. UniProt ID (use primary accession)
    accession = data.get("primaryAccession", uniprot_id)

    # 2. Protein length
    sequence = data.get("sequence", {})
    length = sequence.get("length", "N/A")

    # 3. Organism scientific name
    organism = data.get("organism", {})
    organism_name = organism.get("scientificName", "Unknown Organism")

    # 4. Domain annotations
    # We check features of type "Domain"
    features = data.get("features", [])
    domains = []
    for feature in features:
        if feature.get("type") == "Domain":
            description = feature.get("description")
            location = feature.get("location", {})
            start = location.get("start", {}).get("value", "?")
            end = location.get("end", {}).get("value", "?")
            if description:
                domains.append(f"{description} ({start}-{end})")
            else:
                domains.append(f"Domain ({start}-{end})")

    # Combine domain annotations
    all_domains = "; ".join(domains) if domains else "None"
    return {
        "UniProt ID": accession,
        "Protein Length": length,
        "Organism": organism_name,
        "Domain Annotations": all_domains
    }

def main():
    parser = argparse.ArgumentParser(description="Query UniProt REST API for a list of IDs and output a summary TSV.")
    parser.add_argument("input_file", help="Path to the text file containing UniProt IDs (one per line).")
    parser.add_argument("output_file", help="Path to the output TSV file.")
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist.", file=sys.stderr)
        sys.exit(1)

    print(f"Reading UniProt IDs from {args.input_file}...")
    with open(args.input_file, "r") as f:
        uniprot_ids = [line.strip() for line in f if line.strip()]

    print(f"Found {len(uniprot_ids)} IDs to query.")

    results = []
    headers = ["UniProt ID", "Protein Length", "Organism", "Domain Annotations"]

    for uid in uniprot_ids:
        print(f"Querying {uid}...")
        info = fetch_uniprot_info(uid)
        if info:
            results.append(info)
        else:
            results.append({
                "UniProt ID": uid,
                "Protein Length": "N/A",
                "Organism": "N/A",
                "Domain Annotations": "Error/Not Found"
            })

    print(f"Writing results to {args.output_file}...")
    with open(args.output_file, "w", encoding="utf-8") as f:
        # Write header
        f.write("\t".join(headers) + "\n")
        # Write rows
        for row in results:
            row_data = [str(row[h]) for h in headers]
            f.write("\t".join(row_data) + "\n")

    print("Done!")

if __name__ == "__main__":
    main()
