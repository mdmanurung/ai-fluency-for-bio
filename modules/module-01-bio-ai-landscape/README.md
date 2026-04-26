# Module 1: The Bio-AI Landscape

**Estimated Time to Complete: ~45 mins**

> **Prerequisites:** None. This is the starting point.
> **Tools needed:** None for this module — reading and one browser-based exercise only.

---

## Hook: Same Question, Wrong Tool

A postdoc has just purified a novel bacterial enzyme and wants to know its 3D structure.
She pastes the amino acid sequence into ChatGPT and asks: *"What does this protein look like?"*

ChatGPT returns two paragraphs describing a plausible active site — confident, detailed, entirely fabricated.

Meanwhile, her labmate spends 30 seconds submitting the same sequence to AlphaFold Server.
He gets a high-confidence 3D model back in 20 minutes.

**Same sequence. Same question. Completely different tools — and only one of them was appropriate.**

This module explains why, and gives you a framework to make that call for any task in your workflow.

---

## Part 1: Two Kinds of AI in Biology

The term "AI" in biology currently refers to two fundamentally different families of systems.
Confusing them is the single most common mistake researchers make.

### Predictive AI — Specialist Models

Predictive AI models are trained on large biological datasets to solve **one well-defined problem**.
They output a specific prediction from a specific input type.

| Model | Input | Output |
|-------|-------|--------|
| AlphaFold 2 / 3 | Amino acid sequence | 3D structure (pLDDT confidence) |
| ESMFold | Amino acid sequence | 3D structure (faster, lower accuracy) |
| DeepVariant | Raw sequencing reads | Variant calls (SNPs, indels) |
| Cellpose | Microscopy image | Cell / nucleus segmentation masks |
| Enformer / Basenji | DNA sequence | Gene expression prediction |
| DNABERT | DNA k-mer sequence | Regulatory region classification |

**Key properties:**
- Trained on labeled biological data (PDB structures, VCF files, annotated genomes)
- Deterministic or near-deterministic — same input gives the same output
- Cannot explain reasoning or synthesize text
- Highly reliable within their training distribution; can fail badly outside it

### Generative AI (LLMs) — Generalist Language Models

Large Language Models (LLMs) are trained on enormous corpora of text to predict the next token
in a sequence. They can generate fluent text, write code, answer questions, and summarize documents.

**Examples:** GPT-4o (ChatGPT), Claude 3.5/4, Gemini, Llama 3, Mistral

**Key properties:**
- Trained primarily on text (scientific papers, code, web pages) — not on raw biological data
- Probabilistic — same prompt can produce different outputs
- Can write, explain, summarize, translate, and code across any domain
- Have no dedicated biological "knowledge module" — they pattern-match from training text
- Can hallucinate with complete confidence (see the postdoc's example above)

### Decision Framework: Which Tool for Which Task?

| Task | Use Predictive AI | Use Generative AI (LLM) |
|------|:-----------------:|:-----------------------:|
| Predict protein structure from sequence | ✅ AlphaFold / ESMFold | ❌ Will fabricate |
| Call variants from sequencing reads | ✅ DeepVariant | ❌ Cannot process raw reads |
| Segment cells in fluorescence images | ✅ Cellpose | ❌ Cannot process images this way |
| Summarize a paper's methods section | ❌ No specialist model | ✅ Claude / ChatGPT |
| Write a Biopython script to parse FASTA | ❌ No specialist model | ✅ Claude / ChatGPT |
| Troubleshoot a failed PCR protocol | ❌ No specialist model | ✅ Claude / ChatGPT |
| Synthesize findings across 10 papers | ❌ No specialist model | ✅ Claude + NotebookLM |
| Predict pathogenicity of a novel variant | ✅ AlphaMissense, ClinPred | ⚠️ Unreliable alone |

> **Rule of thumb:** If there is a specialist biological AI model trained specifically for your task,
> use it. LLMs are for language — writing, coding assistance, synthesis, and explanation.

---

## Part 2: Bio-AI Glossary

The following glossary maps AI terminology to biological concepts you already know.
The analogies are imperfect — all analogies are — but they give you a mental foothold.

| AI Term | Plain Definition | Biological Analogy |
|---------|-----------------|-------------------|
| **Token** | Smallest unit of text the model processes (a word fragment, ~4 characters on average) | Codon — a minimal unit of information in a sequence |
| **Tokenization** | Breaking input text into tokens before processing | Reading frame parsing — dividing a sequence into codons |
| **Embedding** | Representing a token as a point in high-dimensional numerical space | Sequence space — sequences with similar function cluster near each other |
| **Parameter / Weight** | A learned numerical value inside the model (GPT-4 has ~1.7 trillion) | Binding affinity / rate constant — a tuned value governing molecular behavior |
| **Pre-training** | Exposing the model to billions of text examples to build general capabilities | Evolutionary selection — accumulating adaptive changes across generations |
| **Fine-tuning** | Adapting a pre-trained model to a specific task using a smaller dataset | Induced fit / specialization — adjusting a generalist to a specific substrate |
| **Context window** | Maximum text the model can "see" in one exchange (e.g., 200,000 tokens for Claude) | Reading frame / promoter window — the region of sequence that is "read" at one time |
| **Hallucination** | Model generating confident but incorrect or fabricated output | Off-target binding / false positive — a plausible-looking result with no biological validity |
| **Prompt** | The input text you send to the model | Ligand / transcription factor — input signal that activates and directs a response |
| **Inference** | Running the trained model to generate a response | Gene expression — executing the encoded instructions to produce an output |
| **Training data** | The corpus of text and data the model learned from | Evolutionary record / reference database — the accumulated information encoded in the system |
| **Foundation model** | A large, general-purpose model used as the base for specialization | Last universal common ancestor (LUCA) — a common origin adapted into many lineages |
| **RAG** (Retrieval-Augmented Generation) | Grounding model responses by retrieving relevant documents at query time | Horizontal gene transfer — importing external information to augment existing capabilities |
| **Attention mechanism** | How the model weighs relationships between all tokens in context | Protein–protein interaction network — determining which parts of a system influence each other |
| **Temperature** | Parameter controlling output randomness (0 = deterministic, 2 = highly variable) | Mutation rate — higher temperature = more variation in outputs |
| **Vector database** | Storage for embeddings used in retrieval (RAG) | Sequence database (GenBank, UniProt) — indexed repository for fast similarity search |
| **Agent** | A model that uses tools and loops to complete multi-step tasks autonomously | Enzyme cascade / signaling pathway — a sequence of coordinated steps toward a goal |
| **Overfitting** | Model memorizes training data; fails on new inputs | Over-specialization — an organism optimized for one niche that cannot adapt to change |
| **Benchmark** | Standardized test measuring model capability on defined tasks | Assay / reference standard — a controlled measurement against a known reference |
| **Multimodal** | A model that can process multiple input types (text, image, audio, sequence) | Pleiotropic gene — one gene (model) with effects across multiple traits (modalities) |

---

## Part 3: Matching Exercise

**Instructions:** Match each AI term (left column) to its biological equivalent (right column).
Try on your own before revealing the answers.

| # | AI Term | Biological Equivalent |
|---|---------|----------------------|
| 1 | Token | A. Protein–protein interaction network |
| 2 | Hallucination | B. Binding affinity / rate constant |
| 3 | Fine-tuning | C. Codon |
| 4 | Parameter / Weight | D. Off-target binding / false positive |
| 5 | Attention mechanism | E. Induced fit / specialization |
| 6 | Temperature | F. Reading frame |
| 7 | Context window | G. Mutation rate |
| 8 | RAG | H. Horizontal gene transfer |
| 9 | Foundation model | I. Last universal common ancestor (LUCA) |
| 10 | Overfitting | J. Over-specialization |

<details>
<summary>View Gold Standard Output</summary>

| # | AI Term | Answer | Why |
|---|---------|--------|-----|
| 1 | Token | **C. Codon** | Both are the minimal discrete unit of meaning in their respective sequence. A codon encodes one amino acid; a token encodes one fragment of meaning. |
| 2 | Hallucination | **D. Off-target binding / false positive** | Both produce a plausible-looking result that passes a surface check but has no valid underlying basis. |
| 3 | Fine-tuning | **E. Induced fit / specialization** | A general pre-trained model is adjusted to a specific task, just as an enzyme's active site adjusts to fit a specific substrate. |
| 4 | Parameter / Weight | **B. Binding affinity / rate constant** | Both are numerical values tuned during a learning/selection process that govern the system's behavior at a fundamental level. |
| 5 | Attention mechanism | **A. Protein–protein interaction network** | Both describe how elements in a system selectively influence each other — the attention score quantifies "how much should token A pay attention to token B," analogous to interaction strength in a PPI network. |
| 6 | Temperature | **G. Mutation rate** | Both control the degree of variation in outputs. High temperature = high randomness in token selection, just as a high mutation rate increases sequence diversity. |
| 7 | Context window | **F. Reading frame** | Both define the window of sequence information that is actively "read" and interpreted at one time. |
| 8 | RAG | **H. Horizontal gene transfer** | Both involve importing external information into a system to augment capabilities that were not present in the original training/genome. |
| 9 | Foundation model | **I. LUCA** | A large general-purpose model that is subsequently adapted into many specialized variants, just as LUCA gave rise to all subsequent biological lineages. |
| 10 | Overfitting | **J. Over-specialization** | A model that memorizes its training data fails on new data, just as an over-specialized organism cannot cope with environmental change. |

**Score guide:**
- 9–10 correct: Ready for Module 2
- 6–8 correct: Re-read Part 2, focus on the terms you missed
- < 6 correct: Work through Part 2 again with the analogies written out in your own words

</details>

---

## Key Takeaways

1. **Predictive AI and Generative AI are different tools for different problems.** Using ChatGPT to predict protein structure is like using a PCR machine to run a western blot.

2. **LLMs have no dedicated biological knowledge module.** Everything they "know" about biology comes from text patterns in training data — which is why they hallucinate structure predictions and fabricate citations.

3. **AI terminology maps cleanly onto biology.** Tokens ≈ codons, fine-tuning ≈ induced fit, hallucination ≈ off-target binding. These analogies make the literature legible.

4. **Specialist models are the right choice when they exist.** AlphaFold for structure, DeepVariant for variant calling, Cellpose for segmentation. LLMs fill the gaps that specialist models cannot cover.

---

## → Next: Module 2 — Biological Data Literacy and AI

[Open Module 2](../module-02-data-literacy/README.md)

*In Module 2, you will learn how AI models actually ingest biological data — what is read, what is ignored, and why pasting a PDB file into ChatGPT produces a confident but hollow answer.*
