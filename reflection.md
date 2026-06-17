# Reflection — Prep Period (Weeks 1–4)

## What I would trust an agent to do in my research

I would trust an agent to write code for data parsing and API queries — tasks with a clear input, a clear output, and a known validation step. 
e.g., fetching morphological trait data from a database, subsetting a specimen table by species, or querying UniProt for protein 
annotations

-> These tasks are mechanical enough that the agent's output can be checked against known reference values before being used downstream.

I would also trust an agent to help with code structure and refactoring -> reorganizing a script, adding argparse, or splitting a monolithic notebook into reusable functions. The risk here is low because the output is immediately readable and testable.


## What I would not trust an agent to do

I would not trust an agent with any step where a silent error would propagate undetected into a downstream analysis. 
e.g., coordinate system handling is the clearest example — GFF vs BED vs VCF conventions 

The same applies to biological interpretation: whether a morphological pattern reflects a true ecomorphological signal or an artifact of the dataset is not something an agent can judge.

I would also not trust an agent to decide which analysis to run, which traits to include, or how to interpret an unexpected result. 

-> These decisions require domain knowledge about ant morphology and Malagasy biogeography that cannot be encoded in a prompt.

## The core lesson

Agent-generated code can run cleanly, print plausible output, and be silently wrong. The habit that matters is not checking whether the code runs, it's checking whether the output is biologically meaningful.
-> Biological invariants are the cheapest validator available.