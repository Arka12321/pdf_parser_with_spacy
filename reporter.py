"""
reporter.py - Pretty prints parsed resume to terminal + saves JSON
"""

import json
from typing import Dict


class ResumeReporter:

    C = {
        "header":  "\033[1;36m",
        "title":   "\033[1;33m",
        "section": "\033[1;32m",
        "value":   "\033[0;97m",
        "missing": "\033[0;31m",
        "tag":     "\033[0;35m",
        "reset":   "\033[0m",
    }

    def color(self, key: str, text: str) -> str:
        return f"{self.C.get(key, '')}{text}{self.C['reset']}"

    def divider(self, char="─", width=65):
        print(self.color("header", char * width))

    def section(self, title: str):
        print(f"\n{self.color('section', f'▶  {title}')}")
        print(self.color("header", "─" * 50))

    def field(self, label: str, value, fallback="Not found"):
        label_str = f"  {label:<20}"
        if value:
            print(f"{label_str}{self.color('value', str(value))}")
        else:
            print(f"{label_str}{self.color('missing', fallback)}")

    # ──────────────────────────────────────────────────────────────

    def print_report(self, data: Dict):
        self.divider("═")
        print(self.color("title", "  📄  RESUME PARSER — Extracted Information"))
        print(self.color("value", f"  File: {data.get('file', '?')}"))
        self.divider("═")

        # Contact
        self.section("👤 Contact Information")
        self.field("Name",    data.get("name"))
        self.field("Email",   data.get("email"))
        self.field("Phone",   data.get("phone"))

        # Links
        self.section("🔗 Online Profiles")
        links = data.get("links", {})
        self.field("LinkedIn", links.get("linkedin"))
        self.field("GitHub",   links.get("github"))
        self.field("Website",  links.get("website"))

        # Skills
        self.section("🛠️  Skills")
        skills = data.get("skills", [])
        if skills:
            row = ""
            for i, skill in enumerate(skills):
                row += self.color("tag", f"[{skill}]") + " "
                if (i + 1) % 5 == 0:
                    print(f"  {row}")
                    row = ""
            if row:
                print(f"  {row}")
            print(f"\n  {self.color('value', str(len(skills)))} skill(s) found.")
        else:
            print(self.color("missing", "  No skills detected."))

        # Education
        self.section("🎓 Education")
        education = data.get("education", [])
        if education:
            for i, edu in enumerate(education, 1):
                print(f"  {i}. {self.color('value', edu.get('degree_line', ''))}")
                if edu.get("institution"):
                    print(f"       Institution : {edu['institution']}")
                if edu.get("year"):
                    print(f"       Year        : {edu['year']}")
        else:
            print(self.color("missing", "  No education details detected."))

        # Experience
        self.section("💼 Work Experience")
        exp = data.get("experience", {})

        total = exp.get("total_years", 0)
        self.field("Total Years",
                   f"{total} year(s)" if total else None,
                   "Could not calculate")

        if exp.get("date_ranges"):
            print("  Date Ranges:")
            for dr in exp["date_ranges"]:
                print(f"    • {dr}")

        if exp.get("job_titles"):
            print("  Job Titles Detected:")
            for t in exp["job_titles"]:
                print(f"    • {t}")

        if exp.get("companies"):
            print("  Companies / Organisations Mentioned:")
            for c in exp["companies"]:
                print(f"    • {c}")

        self.divider("═")
        print()

    def save_json(self, data: Dict, path: str):
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"  ✅  Report saved → {path}\n")
