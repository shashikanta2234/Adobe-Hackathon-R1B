# Persona-Driven PDF Insight Extractor

## Overview

This solution automatically analyzes a collection of PDFs, identifies the most relevant sections for a given persona and job-to-be-done, and outputs the results in a structured JSON format as specified in the Round 1B "Connecting the Dots" challenge.

- **Offline**: All models and dependencies run locally; no network required after build.
- **Fast & Lightweight**: Model size under 100MB (`all-MiniLM-L6-v2`), CPU-only.
- **Generalizable**: Handles diverse document types and personas.

---

## Approach

1. **Parse PDF Outlines:** Extract section titles, page numbers, and text from all documents.
2. **Embedding:** Convert each section and the persona+job query into semantic vector representations using a local sentence embedding model.
3. **Ranking:** Compute similarity between each section and the persona-job query, rank sections by relevance.
4. **Output:** Save the top-ranked sections with metadata and a snippet to `/app/output/output.json`.

All code is modular (see `/src/` directory).

---

## Folder/Project Structure

round1b_project/
├── Dockerfile
├── requirements.txt
├── run.sh
├── README.md
├── approach_explanation.md
└── src/
├── main.py
├── outline_extractor.py
├── utils.py
└── embedding_model/
└── (model files auto-downloaded during docker build)

---

## How to Build and Run

**1. Place Inputs**  
Put all PDFs, plus these two files, in the `<repo_root>/input/` folder:
- `persona.txt` — single-line or multi-line description of the persona
- `job.txt` — single-line or multi-line description of the job-to-be-done


**2. Build Docker Image**

```bash
docker build --platform linux/amd64 -t solution:r1b .

```
or 

```bash
sudo docker build --platform linux/amd64 -t solution:r1b .

```

**3. Run the Container**

```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none solution:r1b

```
or 

```bash
sudo docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none solution:r1b

```
- Will process all PDFs in `/app/input/` and write `/app/output/output.json`.

---

## Dependencies

- Python 3.10+
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)
- [sentence-transformers==2.2.2](https://www.sbert.net/) (`all-MiniLM-L6-v2`)
- numpy

All dependencies will be installed within the container during build.

---

## Output

A single `output.json` containing:
- **metadata** (input document names, persona, job, processing timestamp)
- **extracted_sections** (document, page, section title, importance rank, score)
- **subsection_analysis** (short snippet per top-ranked section)

---

## Notes

- Total processing time for 3–5 PDFs: under 60 seconds (typical).
- Model auto-downloads during Docker build; runs 100% offline.
- Easy to extend for multilingual use (swap in a multilingual MiniLM model if allowed).
- For any issues, check container logs or `output/` for error messages.

---

> Adobe India Hackathon 2025 Round 1B Submission by Hack_coders
