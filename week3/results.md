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

- Dataset: human_nontata_promoters
    - Training samples: 27,097
    - Test samples: 9,034
- Model: InstaDeepAI/nucleotide-transformer-v2-50m-multi-species
    - Embeddings: mean pooling over tokens
    - Random seed: 1908

**Prompt:** *Using the genomic-benchmarks package, load the human_nontata_promoters dataset. Use InstaDeepAI/nucleotide-transformer-v2-50m-multi-species from HuggingFace to extract per-sequence embeddings using mean pooling over tokens. Set all random seeds to 1908 for reproducibility. First test the pipeline on 1000 training sequences and 500 test sequences. Then provide code to scale to the full dataset. Train a logistic regression classifier on the embeddings and report accuracy, F1 score, and a confusion matrix.*

- Embedding: Per-sequence embeddings & Mean pooling over token embeddings
-> So this is a linear probe on top of pretrained genomic representations, not task-specific learning in the encoder


**Reversed Prompt Execution**: Version error corrected & class imbalaced in the first 1000 samples was misleading for the full dataset -> using random sampling of the full dataset for fair comparison.

**Model Performance:**
On Training set size of 1000 samples and test set size of 500 samples:
- Accuracy: 0.6400
- F1: 0.6194
- Confusion matrix: [[179  87]     
                     [ 93 141]]

-> confusion matrix shows fairly symmetric errors → model is not collapsing to majority class, is good

Classification Report:
              precision    recall  f1-score   support

           0       0.66      0.67      0.67       266
           1       0.62      0.60      0.61       234

    accuracy                           0.64       500
   macro avg       0.64      0.64      0.64       500
weighted avg       0.64      0.64      0.64       500

**Distribution of Full Dataset**
Total Train samples: 27097
Total Test samples: 9034
Distribution for Train Dataset:
  Class 0: 14742 samples (54.40%)
  Class 1: 12355 samples (45.60%)
Distribution for Test Dataset:
  Class 0: 4915 samples (54.41%)
  Class 1: 4119 samples (45.59%)

**Model Performance on Full Dataset**
On Training set size of 27,097 samples and test set size of 9,034 samples:
- Accuracy: 0.7192
- F1: 0.6912

Classification Report (Full):
              precision    recall  f1-score   support

           0       0.74      0.74      0.74      4915
           1       0.69      0.69      0.69      4119

    accuracy                           0.72      9034
   macro avg       0.72      0.72      0.72      9034
weighted avg       0.72      0.72      0.72      9034

**Strong signals**

*The result ~0.72 accuracy indicates:*

* The nucleotide transformer embeddings encode promoter-relevant regulatory patterns
* Mean pooling is sufficient to preserve signal (no need for token-level attention pooling for baseline performance)
* Linear separability exists but is incomplete

**Limitation signals:**
* Logistic regression plateau suggests nonlinear structure remains unexploited
* Mean pooling likely loses:
    * motif positional information
    * long-range interactions
    * local promoter architecture (core promoter vs flanking regions)

- Published CNN baseline you compared against: 
    * frozen language-model embedding pipeline (see above) 
    * Most CNN baselines in this benchmark family tend to fall roughly in:

* ~0.70–0.80 accuracy (dataset-dependent and tuning-dependent)

So model is:

* Competitive with classical CNN baselines, but not necessarily exceeding well-tuned ones

- **Interpretation:**
    * Pretrained nucleotide transformers already encode promoter-relevant features
    * A simple linear classifier can recover ~0.72 accuracy on this dataset
    * Scaling data improves performance significantly → embeddings are data-efficient but not trivially separable
    * Pretrained genomic representations + linear probe achieve CNN-level performance without task-specific training

**Fine-Tuning of task C**

~ true end-to-end sequence classification problem

**Prompt:** *Implement a reproducible Colab pipeline to fine-tune InstaDeepAI/nucleotide-transformer-v2-50m-multi-species on the human_nontata_promoters dataset from genomic-benchmarks (binary classification). Set all random seeds to 1908 and ensure deterministic behavior. First test on 1,000 train and 500 test samples (seeded shuffle), then scale to full data (27,097 train / 9,034 test). Tokenize with HuggingFace AutoTokenizer (max length 512, padding + truncation). Fine-tune the full model (no frozen layers) using HuggingFace Trainer with lr=2e-5, batch size=8, 3 epochs, weight decay=0.01, epoch evaluation, and best-model loading. Report accuracy, F1, confusion matrix, and classification report using sklearn/evaluate. After subset validation, rerun on full dataset with identical settings. Include all imports, pip installs, and clean modular Colab code.*




## Surprises

Task C was harder than expected. While I expected the model to perform well, I didn't expect the performance to be so close to the published baselines. I also didn't expect the performance to improve so significantly with the increase in dataset size. 

-> a littel for and back with the AI to get the script that was lokkical for the task and also to understand the output files, esp. a version confict on the genomic benchmark 

But also the low confidence regions of Ubiquitin were surprising. I expected the entire protein to be confidently predicted, but the low confidence regions suggest that there are still some regions of the protein that are not well understood. 

-> but the script run smoothly in general, except the error in task C with the class imbalnce and the version conflict on the genomic benchmark
-> but with the prompt in the end it worked out fine 
-> overall i am happy with the results

