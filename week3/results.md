# Week 3 Results

Use this file for the short Week 3 write-up. Keep it factual: what ran, what failed, what you checked, and what you would trust.

## Exercise A: Structure Prediction

- **Tool or notebook:** Google Colab - AlphaFold2.ipynb
- **Sequence or target:** 
    - Ubiquitin (76 aa): MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG 
- **Mean pLDDT:** Ubiquitin: 95.8 (seed 0) // Ubiquitin: 96.1 (seed 8)
- **Low-confidence regions:** Some residues at the C-terminus and loop regions showed lower pLDDT scores. 
- **PAE observation, if relevant:** PAE values were generally low, indicating high confidence in the predicted structures. 
- **Would you trust this prediction for a biological claim? Why or why not?** - Yes, for the purpose of understanding the general structure and folds of the proteins. However, not for making precise claims about specific residue interactions without experimental validation.

Ubiquitin (seed 0): All five AlphaFold model variants produced highly similar confidence scores (pLDDT 93.9–95.8), suggesting a robust and stable prediction.

The same Ubiquitin sequence was predicted using multiple random seeds (0–7). The resulting structures showed very similar confidence scores, with the top-ranked models having pLDDT values between 95.8 and 96.1. This suggests that the prediction is highly stable and robust to changes in initialization. Only minor variations are expected in flexible regions, while the overall fold remains unchanged.

**Seed comparison:** - Ubiquitin (seed 0) and Ubiquitin (seed 8): core structure stable, terminal loop varies

## Exercise B: Protein Embeddings

- Model: ESM2
- Number of sequences: 64
- Pooling choice:
- Plot files:
- Did known families cluster?
- One validation check you performed:

## Exercise C: Optional Genomic Benchmarks

- Dataset:
- Model:
- Embedding or fine-tuning setup:
- Accuracy:
- F1:
- Confusion matrix:
- Published CNN baseline you compared against:
- Interpretation:

## Surprises

List at least one model output that was hard to interpret and one validation habit you will reuse.
