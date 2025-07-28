import sys, os, time, json
from src.outline_extractor import extract_outline_and_sections
from src.utils import load_embedding_model, embed_text, cosine_similarity

PDF_PATH = "/app/input"
OUTPUT_PATH = "/app/output"

def load_persona_job(persona_path, job_path):
    with open(persona_path, "r") as f:
        persona = f.read().strip()
    with open(job_path, "r") as f:
        job = f.read().strip()
    return persona, job

def process_collection(input_dir, output_dir, persona_str, job_str, model):
    # 1. List PDFs
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]
    doc_sections = []
    section_texts = []
    for pdf_file in pdf_files:
        pdf_full = os.path.join(input_dir, pdf_file)
        outline, section_list = extract_outline_and_sections(pdf_full)  # [(section_title, page, text, docname)]
        for s in section_list:
            doc_sections.append({
                "document": pdf_file,
                "page_number": s['page'],
                "section_title": s['title'],
                "full_text": s['text'],
            })
            section_texts.append(s['title'] + "\n" + s['text'])
    # 2. Embed
    all_sections_emb = embed_text(section_texts, model)
    query = persona_str + "\n" + job_str
    query_emb = embed_text([query], model)[0]
    # 3. Similarity & rankings
    sims = [cosine_similarity(query_emb, emb) for emb in all_sections_emb]
    ranked = sorted(zip(doc_sections, sims), key=lambda x: x[1], reverse=True)
    # 4. Output build (top 5)
    output = {
        "metadata": {
            "input_documents": pdf_files,
            "persona": persona_str,
            "job_to_be_done": job_str,
            "processing_timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }
    for rank, (sec, score) in enumerate(ranked[:5], 1):
        output["extracted_sections"].append({
            "document": sec['document'],
            "page_number": sec['page_number'],
            "section_title": sec['section_title'],
            "importance_rank": rank,
            "score": float(score)
        })
        output["subsection_analysis"].append({
            "document": sec['document'],
            "page_number": sec['page_number'],
            "section_title": sec['section_title'],
            "refined_text": sec['full_text'][:400]  # Snippet
        })
    # 5. Save output
    with open(os.path.join(output_dir, "output.json"), "w") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    persona, job = load_persona_job("/app/input/persona.txt", "/app/input/job.txt")
    model = load_embedding_model("./src/embedding_model/")
    process_collection(PDF_PATH, OUTPUT_PATH, persona, job, model)
    print(f"Processing complete. Output saved to {OUTPUT_PATH}/output.json")
    sys.exit(0)