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

- Model: ESM2 (320-dimensional embeddings)
- Number of sequences: 45
- Pooling choice: mean; over residue embeddings
- Plot files: umap_protein_embeddings.png
- Did known families cluster? Yes, the known families clustered together.
    - Pairwise similarity: Cosine similarities were generally higher within protein families than between different families.
    - UMAP visualization: The embeddings formed biologically meaningful clusters. GPCRs, kinases, immunoglobulins, and oxygen-binding proteins grouped together in distinct regions of the UMAP projection.
- One validation check you performed: I visually inspected the PCA/UMAP projections and confirmed that proteins from the same annotated family clustered together.

Extracted 45 sets of per-residue embeddings.
Shape of first per-residue embedding: (1024, 320)
Extracted 45 per-sequence embeddings.
Shape of first per-sequence embedding: (320,)

UMAP embeddings shape: (45, 2)

**Conclusion:** The ESM2 embeddings capture functional and structural relationships between proteins and could serve as useful input features for downstream classification tasks.

## Exercise C: Optional Genomic Benchmarks

- Dataset:
- Model:

**Prompt:** *Using the genomic-benchmarks package, load the human_nontata_promoters dataset. Use InstaDeepAI/nucleotide-transformer-v2-50m-multi-species from HuggingFace to extract per-sequence embeddings using mean pooling over tokens. Set all random seeds to 42 for reproducibility. First test the pipeline on 1000 training sequences and 500 test sequences. Then provide code to scale to the full dataset. Train a logistic regression classifier on the embeddings and report accuracy, F1 score, and a confusion matrix.*

- Embedding or fine-tuning setup:
- Accuracy:
- F1:
- Confusion matrix:
- Published CNN baseline you compared against:
- Interpretation:

## Surprises

List at least one model output that was hard to interpret and one validation habit you will reuse.
