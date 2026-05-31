# lessons.md — your prep log

One file for the whole prep. Keep two kinds of entry in **separate subsections each week** — don't mix them in one paragraph.

| Subsection | What goes here | How much detail |
|------------|----------------|-----------------|
| **From the materials** | Notes while watching or reading; answers to each week's reflection exercises | Usually one sentence per video chunk or paper section; reflection exercises can be a short paragraph each |
| **Surprises** | Moments an LLM or agent surprised you — good or bad — in chat or in the IDE | Concrete: tool/model, what you asked, what came back, optional takeaway |

Commit and push weekly. By week 4 this file is one of the most useful artifacts you bring to Brno. (`reflection.md` in week 4 is separate — one final paragraph for assessment.)

---

## From the materials — what to write

While watching or reading, stop every ~20 minutes (or after each major section) and add a line answering:

- *Video:* **What's the one thing I'd want to test from what I just heard?**
- *Paper:* **What claim would I most want to verify on my own data?**

Each week may also assign a **reflection exercise** (structured thinking using the week's mental model). Put those answers here too — they are not required to be personal chat logs.

---

## Surprises — what to write

Add an entry whenever an LLM or agent catches you off guard. Include enough detail that you (or a classmate) could understand the moment months later.

- **When** — approximate date
- **Tool / model** — e.g. ChatGPT (free), Claude, Antigravity agent, Cursor, …
- **What you asked** — paste or paraphrase the prompt; name any file or data involved
- **What happened** — the surprising part
- **Takeaway** (optional) — one line on what you'd do differently

**Bad (too vague):** *"ChatGPT hallucinated something."*

**Good:**

> **2026-05-26 · ChatGPT (free, no browsing)** — Asked: *"What is the Ensembl ID for human BRCA1?"* Answered confidently with `ENSG00000012048` — correct — then cited a made-up paper (*Smith et al., Nature 2019*) and a DOI that 404s. **Takeaway:** right gene, invented provenance; never trust citations without checking.

> **2026-06-03 · Antigravity agent** — Asked it to filter a BED file to chr21. Code ran, printed 1,842 lines, looked plausible. Checked: 0-based coordinates on a file the header said was 1-based. **Takeaway:** spot-check coordinate conventions before trusting counts.

---

## Your entries

## Week 1 - What an LLM actually is?

### Deep Dive into LLMs like ChatGPT (Karpathy, 3h31m, Feb 2025) - *what's the one thing I'd want to test from what I just heard?*

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

**Start-Question:**

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

**Start-Question:**
* Generalization of the Long Chains of Thoughts
  * techncally high sucess rate of longer chains of sub-questions & API calls
  * at least 4 consecutive APIs
  
  * Test if a complex Genomic Workflow (Finding Genes + Function; possible alignemnet; KEGG-Workflow)
  * and also if all biological questions work or if the model breaks/haluzination after second/third/forth call

* Slim Prompts -> Cross-Task-Generalization
  * two demonstrations -> silm versions performed better then the full version (documentation + demonstrations)
  * strong cross-talk generalizability -> more useful then natural language documentation in cotext learning in models

### From the Lecture - Domain Expertise — The Internal Validator of AI Quality

What is one example from my own domain where expertise is needed to instruct an LLM, design a model, or validate an AI-generated result?

**Domain expertise in ecomorphological classification of Malagasy ants**

using a Random Forest model to predict ecological niche membership from morphological traits, the model can achieve high accuracy on the training/test split while actually learning a spurious signal
 e.g. ecomorphs happen to cluster by collection locality or taxonomic group rather than by true morphological differentiation 

 -> without domain knowlegde, a high k looks sucessfull (but isn't)

1. **Introducing the LLM** = asking e.g. Claude debug/design RF pipline -> need specification that the ecological variables (Functional Role, Nesting Niche, Foraging Niche) are theoretically independent dimensions; LLM cannot know that DOMINANT as a funcional rolle is a bahavioral/competitive category and not a size one // xplaining why Set A (raw traits) and Set B (size-corrected residuals) represent genuinely different biological questions, not just preprocessing variants

2. **Model Design** = choice to use inverse-frequency weighting (S2) versus random oversampling (S3) versus unweighted training (S1); depends on whether rare ecomorphs in the sample are rare because of genuine biological rarity or because of sampling bias in the museum collections -> LLm cannot thell which one is scientifcally defensible, only implement what I tell 

3. **Validation** = critical checking whether the traits the model weights most heavily (consistently: EL, eye length) are plausible under known ant biology e.g. If the model had instead selected PW (petiole width) as the dominant predictor across all three niche dimensions, that would be a red flag requiring investigation, not just acceptance. A metric alone cannot catch this. Only familiarity with ant morphology and ecomorph theory can.

=> Clever Hans analogy maps directly: a model that achieves 88% trophic niche accuracy by partially tracking body size covariance rather than true ecomorphological signal would look identical in the confusion matrix to a model that learned the right thing

before trusting any classification result in my dataset, I would need to verify that ecomorph membership is not confounded with collection region, collector identity, or taxonomic family representation

e.g. If all Camponotus specimens happen to be labeled "Dominant" and the model is effectively doing genus recognition, the biology is meaningless.

~ domain expertise tells you not just whether a result is numerically acceptable, but whether the right thing was measured at all


### Reflection Excercise

**Hallucinated PMIDs and DOIs**
  * pre-traing optimizes for surface form, not factual accuracy
  * citation strings follws thiht pattern in training data -> model produces somthing that looks right, but fatasising the actual numbers
  * Fix: Tool use & extrenal database queries (fuzzy weight-memory -> verified working memory)

**Sequence Counting Fails due to Tokenization**
  * chunks sequences into multicharacter tokens; no reliable positional correondence
  * arithmetic over this tokens -> looking to a fixed computed budget
  * Helping: Chain-of-thought prompting (more computational steps); but phython script could be better in general with this 

**Confident-but-wrong taxonomy assignments**
  * enough context so the model can sound credible, but training signal could be thin & patchy (e.g. Malagasy Ants Fauna)
  * Problem here could be Swiss-Cheese-Model -> SFT could train the assistant to sound knowledgeable regardless of actual data coverage
  * Usin LLM only as reasoing on reliable produced data;not let it trail of
  
**Own Project: Ant Morphology + Ecological Patterns // Procupine Taxonomy + Morphology**
* Pipline prduces the data & numbers (e.g. R & Phython)
* Model should reasons over them 
* Could lead into the Swiss Cheese Problems
  


### Hands-On Task

**Vanilla Chatbot**: ChatGPT v.5.5 ; Gemini v.3.5 Flash & Grok v.4.3 Beta Fast (free, with account but no Skills.md or Specifications)

**Code Execution**: Claude (free) with analysis tool + personal specifications; ChatGPT v5.5 after prompt 1 & 2 execution; Google AI Studio (Gemini 3.5 Flash, free)

**Prompt**: I have a FASTA file with non-standard headers in this format:
>sp|P68871|HBB_HUMAN Hemoglobin subunit beta OS=Homo sapiens OX=9606 GN=HBB PE=1 SV=2
Write Python code to parse the UniProt accession (P68871), the gene name (HBB), and the organism (Homo sapiens) from this header string.

All three vanilla bots (ChatGPT, Gemini, Grok) generated working code, but the task was too simple to serve as a true comparison, since all the data was already included in the prompt. 

* No one has tested an edge case (missing GN=, multiple headers, empty file)
* No one has verified the output ->  run it by my self and hope for the best 

Claude's framing: The gap isn't "who writes better code" — it's "who knows whether the code is correct."

Surprisingly, ChatGPT and Grok executed code directly within the free tier, which blurs the distinction between vanilla and code execution. A real gap would become apparent with a real file containing inconsistent headers.


**Prompt 2 (revised)**: I'm working with UniProt FASTA headers and want to verify my parsing against the actual UniProt database. Here are three headers with potentially inconsistent formatting:
>sp|P68871|HBB_HUMAN Hemoglobin subunit beta OS=Homo sapiens OX=9606 GN=HBB PE=1 SV=2
>tr|A0A087X1C5|A0A087X1C5_HUMAN Putative uncharacterized protein OS=Homo sapiens OX=9606 PE=4 SV=1
>sp|P00533|EGFR_HUMAN Epidermal growth factor receptor OS=Homo sapiens OX=9606 GN=EGFR PE=1 SV=2

1. Write Python to parse accession, gene name (if present), and organism from all three
2. For each accession, fetch the actual protein name from the UniProt REST API (https://rest.uniprot.org/uniprotkb/{accession}.json) and check if it matches the header
3. Flag any discrepancies

**2026-05-25 ChatGPT** (free, Code Interpreter) called the UniProt REST API for real and found a genuine discrepancy: A0A087X1C5 is currently listed as Cytochrome P450 2D7, not Putative uncharacterized protein — the header was outdated. The result was verified, not guessed.

**2026-05-25 Grok** produced clean, well-structured code — but its sandbox has no internet access (Connection refused). All three API calls failed silently with ⚠️ Could not compare. The code looked correct; the result was useless.

**2026-05-25 Claude** - same limitation as Grok. Sandbox without internet access. Can search the web and fetch URLs as a tool, but cannot make HTTP requests from within executing code. 
Takeaway: Not all code execution is created equal—the sandbox’s internet access makes all the difference for database-dependent tasks.

**2026-05-25 Google AI Studio with Gemini**
Result: A fully interactive web app with a live API connection, batch upload functionality, an export report, and automatically generated test cases (including intentional organism/name mismatches). Took 229 seconds. Takeaway: Gemini AI Studio interprets coding tasks as app-building projects, not as script requests -> useful if you want a tool, surprising if you just wanted code to understand. 

### Suprises - Week 1

Gemini provided two outputs at once without being asked—an interactive app AND a dependency free Python script. 

| Bot | Sandbox Internet | Output | Verified? |
|-----|-----------------|--------|-----------|
| ChatGPT (free) | Yes | Python script | Real discrepancy found |
| Grok (free) | No | Python script | All API calls failed |
| Claude (free) | No | Python script + edge case test | Same sandbox limit |
| Gemini AI Studio (free) | Yes | Interactive app + Python script | Live API connected |


----

## Week 2 - Agentic IDEs on bioinformatics tasks

###  Software Is Changing (Again) (Karpathy, 40m, 2025) - *what's the one thing I'd want to test from what I just heard?*

~ outlines a fundamental shift in how software is created and utilized, moving from traditional coding to an era of programmable intelligence

**The Three Paradigms of Software:**

**Software 1.0:** traditional code humans write directly for computers to carry out digital tasks

**Software 2.0:** neural networks -> instead of writing code, humans tune data sets and run optimizers to create the parameter of a neural net

**Software 3.0:** Large Language Models (LLMs) -> new kind of programmable computer [paradigm, English is the programming language, and prompts are the programs]

=> LLMs = New Operating System "..LLMs are not just utilities like electricity; they are closer to operating systems."

e.g. Hardware Analogies: LLM acts as a CPU equivalent -> compute and problem-solving, & context window serves as working memory

Ecosytem Evolution: splitting in **closed-source providers** (like OpenAI or Anthropic) and **open-source alternatives** (like the Llama ecosystem)

**The "Psychology" of LLMs**

* (+): possess encyclopedic knowledge and memory, capable of recalling vast amounts of information far beyond human capacity

* (-): hallucinations, "jagged intelligence" (making mistakes no human would make), and anterograde amnesia

**Concept of the "autonomy slider"**

* advocates for apps that combine traditional manual interfaces with LLM integration,rather than fully autonomous agent
* GUI for Verification -> LLMs are fallible, Graphic User Interfaces (GUIs) are essential

**Building for Agents** - AI agents become primary consumers of digital information

1. **Machine-Readable Docs**: Documentation should be provided in formats like markdown rather than just human-centric web pages
2. **Agent Protocols**: like the Model Context Protocol and simple files like llm.txt that help agents understand a website's purpose without having to parse complex HTML
3. **Replacing "Click" with "Curl"**: documentation must replace human-centric instructions (like "click here") with programmable commands (like curl) that an agent can execute
   

#### Yao et al., 2023 ReAct: Synergizing Reasoning and Acting in Language Models - *what claim in this paper would I most want to verify on my own data?*

-> introduces large language models (LLMs) to solve complex tasks by combining reasoning traces and task-specific actions

**Concept:**

* built on the idea that human intelligence combines task-oriented actions with verbal reasoning to strategize and handle exceptions
* augmenting the LLM’s action space to include a "language space" (thoughts), the model can generate "reasoning traces"
* help induce, track, and update action plans
* thoughts do not affect the environment but instead help the model manage its own internal "working memory" & reasoning process

=> Overcoming Limitations of Prior Methods 

* Cahin of Thoughts only (good internal reasoning; not grounded in extrenal refrences) -> fact hallucination
* Act only -> lack the ability of reason & maintain working memory

**ReAct - Testing across 4 Benchmarks**

1. question answering (HotpotQA)
2. fact verification (Fever)
3. text-based games (ALFWorld)
4. web navigation (WebShop)

* HotpotQA and Fever, ReAct overcomes hallucination by interacting with a Wikipedia API to ground its reasoning in factual data
* ALFWorld and WebShop, ReAct outperformed imitation and reinforcement learning methods by 34% and 10% absolute success rates

=> best results often came from combining ReAct and CoT-SC (Self-Consistency), which allows the model to use its internal knowledge when confident and back off to external search (ReAct) when it is not

=> Human-in-the-loop ~ makes the model's decision-making process more interpretable, trustworthy, and diagnosable

* few-shot prompting showed strong results
* finetuning smaller models (like PaLM-8B or 62B) on ReAct trajectories significantly improved their performance -> "Finetuned ReAct models outperformed those trained only on "Standard" or "CoT" formats because they were taught the generalizable skill of how to reason and act to access information, rather than just memorizing facts"
  

### From the Lecture - Feature Engineering: Translating Scientific Intuition into Numbers


### Guided Exercises


### Trap Exercise


#### Discussion Questions

*What other "looks right but isn't" failures might hide in agent-generated bioinformatics code? (Strand handling, GRCh37/38 confusion, BED vs GFF, 0-based vs 1-based VCF positions, samtools mpileup off-by-one, BAM flag bitfield misreads, phred encoding…)*


*For your own subfield, what are three biological invariants you could routinely use to validate agent output?*


*If you had ten thousand CDS features and couldn't eyeball them all, how would you scale this validation?*


### Mini-Project

1. Small CLI tool that takes a list of UniProt IDs and produces a summary table (length, organism, domain annotations) via the UniProt REST API.

2. Script that reads a FASTQ file and produces basic QC stats with a one-page HTML report.



### Suprises - Week 2