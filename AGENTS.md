# AGENTS.md

## Repo structure
- week2/ — exercises and mini-projects from week 2 (FASTQ QC, UniProt, trap exercise)
- week3/ — exercises from week 3 (exA, exB, exC)
- exercises/ — additional exercise materials
- weeks/ — weekly cheatsheets and task descriptions
- onsite/ — materials for the Brno in-person week
- lessons.md — running log of observations and reflections (do not auto-edit)

## Python
- Use Python 3.13.x
- Use pip for package management
- Do not use conda unless explicitly asked

## Data files
- Do not commit large data files (> 1MB)
- Do not commit API keys or credentials
- Raw data and test files live in the relevant week subfolder

## Conventions
- Scripts should accept input and output paths as command-line arguments
- Output format is TSV unless the task requires otherwise
- Print progress to stdout, errors to stderr
- Keep scripts self-contained and runnable from the repo root

## Validation
- Always test scripts on a small known example before claiming success
- Check output against at least one known reference value
- For biological data: apply domain-specific invariants before accepting output

## Do not touch
- Do not edit lessons.md — written by the human only
- Do not modify .gitignore unless explicitly asked
- Do not commit binary files unless explicitly asked