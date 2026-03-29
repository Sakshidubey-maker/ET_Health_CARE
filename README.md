# 🏥 Healthcare Coding Agent (Groq)

## 📌 Description
This project is an AI-powered Healthcare Coding Agent that processes clinical notes, extracts diagnoses and procedures, maps them to ICD-10 and CPT codes, and generates rule-based approval decisions with an audit trail.

## 🚀 Features
- LLM-based extraction (Groq)
- ICD-10 & CPT code mapping
- Rule-based validation
- Decision engine (Approved / Denied)
- Audit output in JSON
- Gradio UI

## 🧠 Tech Stack
- Python
- Gradio
- Groq API
- JSON / Rule Engine

## ▶️ Run Locally
pip install -r requirements.txt  
python app.py  

## 🌐 Live Demo
https://sakshi63-techbuzz.hf.space/

## 📊 Example Input
Patient has fever and cough. Diagnosed with pneumonia. Chest X-ray performed.

## 📤 Output
- Diagnoses
- Procedures
- ICD-10 codes
- CPT codes
- Decision (Approved/Denied)

## 🔮 Future Improvements
- Real ICD/CPT dataset (RAG)
- Multi-payer rules
- Better UI visualization
- Deployment at scale
