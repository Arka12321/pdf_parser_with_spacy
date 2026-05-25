"""
main.py - Resume Parser Entry Point
Usage:
    python3 main.py                          # parse sample resume
    python3 main.py path/to/your_resume.pdf  # parse your own PDF
"""

import sys
import os

# Make sure imports work from any directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parser   import ResumeParser
from reporter import ResumeReporter


def main():
    print("\n" + "="*65)
    print("   📄  RESUME PARSER — Powered by spaCy + pypdf")
    print("="*65 + "\n")

    # ── Determine which PDF to parse
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        # Use sample resume (generate it if missing)
        pdf_path = "sample_resumes/sample_resume.pdf"
        if not os.path.exists(pdf_path):
            print("  ℹ️  No PDF provided. Generating sample resume...\n")
            from generate_sample_resume import generate
            generate()
            print()

    if not os.path.exists(pdf_path):
        print(f"  ❌  File not found: {pdf_path}")
        print("  Usage: python3 main.py path/to/resume.pdf")
        sys.exit(1)

    # ── Parse
    parser   = ResumeParser(model="en_core_web_sm")
    reporter = ResumeReporter()

    data = parser.parse(pdf_path)

    # ── Print to terminal
    reporter.print_report(data)

    # ── Save JSON
    os.makedirs("outputs", exist_ok=True)

    # Make a clean filename from the PDF name
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    json_path = f"outputs/{base_name}_parsed.json"

    reporter.save_json(data, json_path)

    print("  🎉  Done!\n")
    print("  To parse your own resume:")
    print("  python3 main.py /path/to/your_resume.pdf\n")


if __name__ == "__main__":
    main()
