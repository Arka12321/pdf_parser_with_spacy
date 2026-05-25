# 📄 Resume Parser — spaCy + pypdf

Automatically extracts structured information from PDF resumes
using spaCy NLP and regex pattern matching.

---

## 📁 Project Structure

```
resume_parser/
├── main.py                    # Entry point ← RUN THIS
├── parser.py                  # Core extraction engine (spaCy + pypdf)
├── reporter.py                # Terminal output + JSON saver
├── generate_sample_resume.py  # Generates a test resume PDF
├── sample_resumes/
│   └── sample_resume.pdf      # Auto-generated test resume
└── outputs/
    └── sample_resume_parsed.json  # Auto-saved results
```

---

## 🚀 Setup

```bash
# 1. Activate your virtual environment
source /home/partha/Desktop/.venv/bin/activate

# 2. Install dependencies
pip install spacy pypdf reportlab

# 3. Download spaCy model
python3 -m spacy download en_core_web_sm
```

---

## ▶️ Run

```bash
cd /home/partha/Desktop/resume_parser

# Parse the auto-generated sample resume
python3 main.py

# Parse YOUR own resume
python3 main.py /path/to/your_resume.pdf
```

---

## 📊 What Gets Extracted

| Field         | Method Used              | Example Output              |
|---------------|--------------------------|-----------------------------|
| Name          | spaCy PERSON entity      | Arjun Sharma                |
| Email         | Regex                    | arjun@gmail.com             |
| Phone         | Regex                    | +91-9876543210              |
| LinkedIn      | Regex URL match          | linkedin.com/in/arjun       |
| GitHub        | Regex URL match          | github.com/arjun            |
| Skills        | Keyword database match   | Python, React, AWS, Docker  |
| Education     | Degree keyword + NER     | B.Tech, IIT Bombay, 2019    |
| Experience    | Date range regex + NER   | 4 years, Infosys, Wipro     |
| Job Titles    | Regex patterns           | Senior Software Engineer    |

---

## 💡 Tips

- Works best with **text-based PDFs** (not scanned images)
- For scanned PDFs, run OCR first using `pytesseract`
- Add more skills to `SKILLS_DB` in `parser.py` for better detection
- Switch to `en_core_web_md` for better name/org recognition
