# **Lessons Learned Summer School Brno 2026**

## Week 1 - What an LLM actually is?

#### Deep Dive into LLMs like ChatGPT (Karpathy, 3h31m, Feb 2025) - *what's the one thing I'd want to test from what I just heard?*

* LLM's -> proabilistic text simulator
* Mental Model of LLM: Predictor of the next token based on patterns in a text corpus.

Step 1: Pre-Traing -> Creates Knowledge Base

* model consumes internet sources
* learns stat. relationships
* continuation

Step 2: Post-Traing -> Supervised Fine-Tuning (SFT)
* curated assitant interactions results in curated dialogue datasets; humnan labels; policy conditioning
  
Hallucinations & Reasoning
* Hallucinations happens because of: partial pattern; confidence & correctness decoupled
* Reasoning means generating the "Tokens"
    * Models do better ehen: think step by step; bachtracking & explore alternatives
    * so "think step-by-step"; "show you reasoning" working good

Reinforcement Learning from Human Feedback (RLHF)
* trains model to optimize for human performance signas
  
Tokenization
* translationg between rwa text strings & tokens (text chunks) -> represents unique integer IDs
* Representation: text as bytes -> possible values of 1 byte (256); so representing a long text long sequence => using tokenization for copressing
* Byte Pair Encoding: identifies commen consecutive pairs of bytes/symboles -> merge into a signle new symbole
* output: one-dimensional sequence of these symbole IDs (unique identfiers)
* Problem: weakness in counting letters; spelling backwards; exact charcter manipulation
=> model is operating on sub-chunks, not symbolic characters
=> Example: "Strawberry" Counting
  * translating raw text into tokens 
  * effectively loses sight of the indvidual charcters
  * invsible letters -> 3 "r"'s hidden inside those token IDs -> model guess
  * "Jagged Edge" -> viral Problem (AI can solve complex Problems in maths/physics but fails at simple counting task)

LLM intelligence is uneven -> "Swiss Cheese Intelligence"
* can do garduate level problems & summarize complex reaserach, but failes at simpler task & logic edge cases

Answer Start-Question:

- Jagged Edges / Swiss Cheese Capability Model 
- whether "reasoning" in LLMs is a just token-space search over patterns or somthing deeper emerges when thinking is involved 

### Jin et al., 2024 GeneGPT: Argmenting Large Language Models with Domain Tolls for Improved Access to Biomedical Information - *what claim in this paper would I most want to verify on my own data?*

GeneGPT - teaches models to use real world tools like NCBI Web API

The Problem -> is Knowledge of the LLM vs Precision
The Solution -> Tool augmenation (allows model to look up information in extrenal databases)

How GeneGPT works?

- in-context learning -> model provided with a prompt containing a few concrete demonstrations
- TRIGGER: trained to generate a specific symbole (here ->) when need extrenal data
- EXECUTION: Stop -> extract the URLs -> calls the NCBI API -> feeds back the results
- DECODING: as freh data in working memory -> provide a precise & fact-based answer

=> Agentic Concept of Multi-Hop Reasoning 

Example: SNP-Gene-Function

* calls an API to find gene name assosiated with SNP
* uses results create second API to find the gene function
* etc.

Most coomon errors:

* E1: wrong API / not unsing API
* E2: Right API -> wrong arguments (e.g. Sequence Gene Alias; ~30 cases)
* E3: Failure to encode the answer (e.g. SNP gene function; ~29 cases)
* E4: Unanswerable with NCBI databases (e.g. Simple tasks of Location and Alias 17/50 questions Error)


#### Reflection Excercise