import os
import json
import re
import gradio as gr
from dotenv import load_dotenv
from groq import Groq

# Load API key
load_dotenv()
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))
client = Groq(api_key=os.getenv("KEY"))

# --- Mock Code Dictionaries ---
ICD_CODES = {
    "pneumonia": "J18.9",
    "fever": "R50.9",
    "cough": "R05",
    "headache": "R51"
}

CPT_CODES = {
    "chest x-ray": "71045"
}

# --- Clean JSON from LLM ---
def clean_json(text):
    text = re.sub(r"```json|```", "", text).strip()
    return json.loads(text)

# --- LLM Extraction ---
def extract_entities(note):
    prompt = f"""
    Extract diagnoses and procedures from this clinical note.

    Note:
    {note}

    Return ONLY valid JSON:
    {{
        "diagnoses": [],
        "procedures": []
    }}
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    text = response.choices[0].message.content

    try:
        return clean_json(text)
    except:
        return {"diagnoses": [], "procedures": []}

# --- Mapping ---
def map_codes(extracted):
    diagnoses = [ICD_CODES.get(d.lower(), "UNKNOWN") for d in extracted["diagnoses"]]
    procedures = [CPT_CODES.get(p.lower(), "UNKNOWN") for p in extracted["procedures"]]
    return diagnoses, procedures

# --- Rule Engine ---
def apply_rules(diagnoses, procedures):
    result = {"approved": True, "issues": []}

    if "71045" in procedures and "J18.9" not in diagnoses:
        result["approved"] = False
        result["issues"].append("Chest X-ray requires pneumonia diagnosis")

    if len(diagnoses) == 0:
        result["approved"] = False
        result["issues"].append("No diagnosis provided")

    return result

# --- Full Pipeline ---
def process_note(note):
    extracted = extract_entities(note)
    diagnoses, procedures = map_codes(extracted)
    rules = apply_rules(diagnoses, procedures)

    audit = {
        "input_note": note,
        "extracted_entities": extracted,
        "ICD-10": diagnoses,
        "CPT": procedures,
        "decision": "APPROVED" if rules["approved"] else "DENIED",
        "issues": rules["issues"]
    }

    return json.dumps(audit, indent=2)

# --- Gradio UI ---
ui = gr.Interface(
    fn=process_note,
    inputs=gr.Textbox(lines=8, label="Clinical Note"),
    outputs=gr.Code(label="Audit Output (JSON)"),
    title="🏥 Healthcare Coding Agent (Groq)",
    description="Enter a clinical note to get ICD-10, CPT, and approval decision."
)

if __name__ == "__main__":
    ui.launch()
