"""
parser.py - Core Resume Parser Engine
Extracts: Name, Email, Phone, Skills, Education, Experience, Links
Uses: spaCy (NLP) + pypdf (PDF reading) + regex (pattern matching)
"""

import spacy
import re
from pypdf import PdfReader
from typing import Dict, List, Optional


class ResumeParser:

    # ── Master skills list (add more as needed)
    SKILLS_DB = [
        # Programming Languages
        "python", "java", "javascript", "c++", "c#", "ruby", "php",
        "swift", "kotlin", "golang", "rust", "typescript", "scala",
        "r", "matlab", "perl", "bash",
        # Web Development
        "html", "css", "react", "angular", "vue", "nodejs", "django",
        "flask", "fastapi", "spring", "bootstrap", "jquery", "nextjs",
        "express", "laravel",
        # Databases
        "sql", "mysql", "postgresql", "mongodb", "redis", "sqlite",
        "oracle", "cassandra", "firebase", "elasticsearch",
        # Data Science / AI / ML
        "machine learning", "deep learning", "nlp", "computer vision",
        "tensorflow", "pytorch", "keras", "scikit-learn", "pandas",
        "numpy", "matplotlib", "seaborn", "spacy", "nltk", "opencv",
        "data analysis", "data visualization",
        # Cloud & DevOps
        "aws", "azure", "gcp", "docker", "kubernetes", "jenkins",
        "git", "github", "gitlab", "linux", "terraform", "ansible",
        "ci/cd", "rest api", "graphql",
        # Tools & Other
        "excel", "tableau", "power bi", "figma", "photoshop",
        "jira", "confluence", "postman", "agile", "scrum",
    ]

    DEGREE_KEYWORDS = [
        "b.tech", "btech", "b.e", "be", "bachelor", "b.sc", "bsc",
        "m.tech", "mtech", "master", "m.sc", "msc", "mba", "ph.d",
        "phd", "doctorate", "diploma", "10th", "12th", "ssc", "hsc",
        "intermediate", "b.com", "bcom", "b.ca", "bca",
    ]

    EXPERIENCE_HEADERS = [
        "experience", "work experience", "employment",
        "internship", "professional experience", "career",
    ]

    EDUCATION_HEADERS = [
        "education", "academic", "qualification",
        "educational background", "schooling",
    ]

    def __init__(self, model: str = "en_core_web_sm"):
        print(f"[ResumeParser] Loading spaCy model '{model}'...")
        self.nlp = spacy.load(model)
        print("[ResumeParser] Ready!\n")

    # ────────────────────────────────────────────────────────────
    # 1. READ PDF
    # ────────────────────────────────────────────────────────────
    def read_pdf(self, pdf_path: str) -> str:
        """Read all text from a PDF file using pypdf."""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text.strip()
        except Exception as e:
            raise ValueError(f"Could not read PDF '{pdf_path}': {e}")

    # ────────────────────────────────────────────────────────────
    # 2. EXTRACT NAME
    # ────────────────────────────────────────────────────────────
    def extract_name(self, raw_text: str) -> Optional[str]:
        """
        Find candidate name from top 5 lines.
        Strategy: spaCy PERSON entity first, then fallback to
        first short alphabetic line (likely the name header).
        """
        first_lines = "\n".join(raw_text.strip().split("\n")[:5])
        doc = self.nlp(first_lines)

        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text.strip()

        # Fallback: first short line with only letters/spaces
        for line in raw_text.split("\n"):
            line = line.strip()
            if line and len(line.split()) <= 5:
                if re.match(r"^[A-Za-z\s\.]+$", line):
                    return line

        return None

    # ────────────────────────────────────────────────────────────
    # 3. EXTRACT EMAIL
    # ────────────────────────────────────────────────────────────
    def extract_email(self, text: str) -> Optional[str]:
        """Regex match for standard email format."""
        match = re.search(
            r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", text
        )
        return match.group(0) if match else None

    # ────────────────────────────────────────────────────────────
    # 4. EXTRACT PHONE
    # ────────────────────────────────────────────────────────────
    def extract_phone(self, text: str) -> Optional[str]:
        """
        Matches formats like:
        +91-9876543210 | 9876543210 | (987) 654-3210 | 98765 43210
        """
        patterns = [
            r"(\+91[\s\-]?)?\d{10}",
            r"(\+?\d{1,3}[\s\-]?)?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4}",
            r"\d{5}[\s\-]\d{5}",
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                phone = match.group(0).strip()
                digits = re.sub(r"\D", "", phone)
                if len(digits) >= 10:
                    return phone
        return None

    # ────────────────────────────────────────────────────────────
    # 5. EXTRACT SKILLS
    # ────────────────────────────────────────────────────────────
    def extract_skills(self, text: str) -> List[str]:
        """
        Match resume text against SKILLS_DB using word boundaries
        so 'r' doesn't match inside 'array', etc.
        Returns alphabetically sorted unique list.
        """
        text_lower = text.lower()
        found = set()
        for skill in self.SKILLS_DB:
            pattern = r"\b" + re.escape(skill) + r"\b"
            if re.search(pattern, text_lower):
                found.add(skill.title())
        return sorted(found)

    # ────────────────────────────────────────────────────────────
    # 6. EXTRACT EDUCATION
    # ────────────────────────────────────────────────────────────
    def extract_education(self, text: str, doc: spacy.tokens.Doc) -> List[Dict]:
        """
        Finds lines containing degree keywords.
        Also tries to extract institution name and graduation year.
        """
        education = []
        lines = text.split("\n")

        # Try to isolate just the education section
        edu_section = ""
        in_edu = False
        for line in lines:
            ll = line.lower().strip()
            if any(h in ll for h in self.EDUCATION_HEADERS):
                in_edu = True
            elif in_edu and any(h in ll for h in self.EXPERIENCE_HEADERS):
                in_edu = False
            if in_edu:
                edu_section += line + "\n"

        search_text = edu_section if edu_section.strip() else text

        for line in search_text.split("\n"):
            ll = line.lower()
            if any(deg in ll for deg in self.DEGREE_KEYWORDS):
                # Year
                year_match = re.search(r"(19|20)\d{2}", line)
                year = year_match.group(0) if year_match else None

                # Institution via spaCy NER
                line_doc = self.nlp(line)
                institution = None
                for ent in line_doc.ents:
                    if ent.label_ in ("ORG", "GPE"):
                        institution = ent.text.strip()
                        break

                entry = {
                    "degree_line": line.strip(),
                    "institution": institution,
                    "year":        year,
                }
                if entry["degree_line"] and entry not in education:
                    education.append(entry)

        return education[:5]

    # ────────────────────────────────────────────────────────────
    # 7. EXTRACT EXPERIENCE
    # ────────────────────────────────────────────────────────────
    def extract_experience(self, text: str, doc: spacy.tokens.Doc) -> Dict:
        """
        Extracts:
        - Total years (summed from date ranges like 2019-2023)
        - Date ranges found
        - Companies (spaCy ORG entities)
        - Job titles (regex)
        """
        year_pattern = (
            r"(20\d{2}|19\d{2})\s*[\-–to]+\s*"
            r"(20\d{2}|19\d{2}|present|current|now)"
        )
        matches = re.findall(year_pattern, text.lower())

        total_years = 0
        date_ranges = []
        CURRENT_YEAR = 2025

        for start, end in matches:
            try:
                s = int(start)
                e = CURRENT_YEAR if end in ("present", "current", "now") else int(end)
                diff = e - s
                if 0 < diff < 50:
                    total_years += diff
                    date_ranges.append(f"{start} – {end}")
            except ValueError:
                pass

        # Companies from spaCy ORG entities
        companies = []
        for ent in doc.ents:
            if ent.label_ == "ORG":
                name = ent.text.strip()
                if name not in companies and len(name) > 2:
                    companies.append(name)

        # Job titles via regex
        title_pattern = (
            r"(software engineer|web developer|data scientist|"
            r"data analyst|business analyst|product manager|"
            r"project manager|machine learning engineer|"
            r"ml engineer|ai engineer|devops engineer|"
            r"backend developer|frontend developer|full stack developer|"
            r"mobile developer|android developer|ios developer|"
            r"ui/ux designer|graphic designer|intern|consultant|"
            r"senior engineer|junior developer|tech lead|team lead)"
        )
        raw_titles = re.findall(title_pattern, text.lower())
        titles = list(dict.fromkeys([t.title() for t in raw_titles]))

        return {
            "total_years": total_years,
            "date_ranges": date_ranges,
            "companies":   companies[:8],
            "job_titles":  titles[:5],
        }

    # ────────────────────────────────────────────────────────────
    # 8. EXTRACT LINKS
    # ────────────────────────────────────────────────────────────
    def extract_links(self, text: str) -> Dict:
        """Extract LinkedIn, GitHub, and personal website URLs."""
        linkedin = re.search(r"linkedin\.com/in/[\w\-]+",     text, re.I)
        github   = re.search(r"github\.com/[\w\-]+",          text, re.I)
        website  = re.search(r"https?://(?!linkedin|github)[\w\./\-]+", text, re.I)
        return {
            "linkedin": linkedin.group(0) if linkedin else None,
            "github":   github.group(0)   if github   else None,
            "website":  website.group(0)  if website  else None,
        }

    # ────────────────────────────────────────────────────────────
    # MAIN PARSE METHOD
    # ────────────────────────────────────────────────────────────
    def parse(self, pdf_path: str) -> Dict:
        """
        Full pipeline:
          read PDF → run spaCy → extract all fields → return dict
        """
        print(f"[ResumeParser] Parsing: {pdf_path}")
        raw_text = self.read_pdf(pdf_path)

        if not raw_text.strip():
            raise ValueError(
                "No text found in PDF. It may be a scanned image resume.\n"
                "Tip: Use a PDF with selectable text, or run OCR first."
            )

        print(f"[ResumeParser] {len(raw_text)} characters extracted from PDF.")
        print(f"[ResumeParser] Running spaCy NLP...")
        doc = self.nlp(raw_text)

        result = {
            "file":       pdf_path,
            "name":       self.extract_name(raw_text),
            "email":      self.extract_email(raw_text),
            "phone":      self.extract_phone(raw_text),
            "links":      self.extract_links(raw_text),
            "skills":     self.extract_skills(raw_text),
            "education":  self.extract_education(raw_text, doc),
            "experience": self.extract_experience(raw_text, doc),
        }

        print(f"[ResumeParser] Parsing complete!\n")
        return result
