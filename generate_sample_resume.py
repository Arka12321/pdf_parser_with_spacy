"""
generate_sample_resume.py
Generates a realistic sample resume PDF for testing the parser.
Run this once to create: sample_resumes/sample_resume.pdf
Requires: pip install reportlab
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib import colors
import os


def generate():
    os.makedirs("sample_resumes", exist_ok=True)
    path = "sample_resumes/sample_resume.pdf"

    doc = SimpleDocTemplate(
        path, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()

    name_style = ParagraphStyle(
        "Name", fontSize=20, fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1a1a2e"), spaceAfter=4
    )
    contact_style = ParagraphStyle(
        "Contact", fontSize=10, fontName="Helvetica",
        textColor=colors.HexColor("#444444"), spaceAfter=2
    )
    section_style = ParagraphStyle(
        "Section", fontSize=13, fontName="Helvetica-Bold",
        textColor=colors.HexColor("#16213e"), spaceBefore=14, spaceAfter=4
    )
    body_style = ParagraphStyle(
        "Body", fontSize=10, fontName="Helvetica",
        textColor=colors.HexColor("#333333"), spaceAfter=4, leading=14
    )
    bullet_style = ParagraphStyle(
        "Bullet", fontSize=10, fontName="Helvetica",
        textColor=colors.HexColor("#333333"), spaceAfter=3,
        leftIndent=15, leading=14
    )

    story = []

    # ── Header
    story.append(Paragraph("Arjun Sharma", name_style))
    story.append(Paragraph("arjun.sharma@gmail.com  |  +91-9876543210", contact_style))
    story.append(Paragraph("linkedin.com/in/arjunsharma  |  github.com/arjunsharma", contact_style))
    story.append(Paragraph("Bangalore, Karnataka, India", contact_style))
    story.append(HRFlowable(width="100%", thickness=1.5,
                             color=colors.HexColor("#16213e"), spaceAfter=8))

    # ── Summary
    story.append(Paragraph("Professional Summary", section_style))
    story.append(Paragraph(
        "Passionate Software Engineer with 4 years of experience in full stack "
        "development, machine learning, and cloud infrastructure. Proficient in "
        "Python, React, and AWS. Strong background in building scalable web "
        "applications and data pipelines. Seeking challenging roles in AI/ML "
        "product development.",
        body_style
    ))

    # ── Skills
    story.append(Paragraph("Skills", section_style))
    story.append(Paragraph(
        "<b>Programming:</b> Python, JavaScript, TypeScript, Java, SQL, Bash",
        body_style
    ))
    story.append(Paragraph(
        "<b>Web:</b> React, NodeJS, Django, Flask, FastAPI, HTML, CSS, REST API",
        body_style
    ))
    story.append(Paragraph(
        "<b>Data Science:</b> Machine Learning, Deep Learning, NLP, Pandas, "
        "NumPy, TensorFlow, PyTorch, Scikit-Learn, Matplotlib",
        body_style
    ))
    story.append(Paragraph(
        "<b>Cloud & DevOps:</b> AWS, Docker, Kubernetes, Git, GitHub, Jenkins, Linux",
        body_style
    ))
    story.append(Paragraph(
        "<b>Databases:</b> MySQL, PostgreSQL, MongoDB, Redis, Firebase",
        body_style
    ))
    story.append(Paragraph(
        "<b>Tools:</b> Jira, Postman, Figma, Tableau, Power BI, Agile, Scrum",
        body_style
    ))

    # ── Experience
    story.append(Paragraph("Work Experience", section_style))

    story.append(Paragraph(
        "<b>Senior Software Engineer</b> — Infosys Ltd, Bangalore",
        body_style
    ))
    story.append(Paragraph("2022 – present", bullet_style))
    story.append(Paragraph("• Built scalable REST APIs using Django and FastAPI serving 500K+ requests/day.", bullet_style))
    story.append(Paragraph("• Led a team of 5 developers to migrate legacy monolith to microservices on AWS.", bullet_style))
    story.append(Paragraph("• Reduced API response time by 40% through Redis caching and query optimization.", bullet_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>Software Developer</b> — Wipro Technologies, Hyderabad",
        body_style
    ))
    story.append(Paragraph("2020 – 2022", bullet_style))
    story.append(Paragraph("• Developed frontend features using React and TypeScript for a SaaS dashboard.", bullet_style))
    story.append(Paragraph("• Integrated machine learning models into production pipelines using Python.", bullet_style))
    story.append(Paragraph("• Deployed containerised applications using Docker and Kubernetes on GCP.", bullet_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>ML Intern</b> — Tata Consultancy Services (TCS), Pune",
        body_style
    ))
    story.append(Paragraph("2019 – 2020", bullet_style))
    story.append(Paragraph("• Built NLP pipeline for customer sentiment analysis using spaCy and NLTK.", bullet_style))
    story.append(Paragraph("• Trained deep learning classification model achieving 91% accuracy on test set.", bullet_style))

    # ── Education
    story.append(Paragraph("Education", section_style))
    story.append(Paragraph(
        "<b>B.Tech in Computer Science</b> — Indian Institute of Technology (IIT) Bombay",
        body_style
    ))
    story.append(Paragraph("Graduated: 2019  |  CGPA: 8.7/10", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>12th (HSC)</b> — Delhi Public School, New Delhi  |  2015  |  94.6%",
        body_style
    ))
    story.append(Paragraph(
        "<b>10th (SSC)</b> — Delhi Public School, New Delhi  |  2013  |  96.2%",
        body_style
    ))

    # ── Projects
    story.append(Paragraph("Notable Projects", section_style))
    story.append(Paragraph(
        "<b>NewsAI</b> — Built a real-time news aggregator with NLP-based topic "
        "classification and sentiment analysis using Python, spaCy, and React.",
        body_style
    ))
    story.append(Paragraph(
        "<b>SmartResume</b> — Developed an AI-powered resume parser using spaCy "
        "and PyTorch that extracts structured data from PDF resumes with 95% accuracy.",
        body_style
    ))

    # ── Certifications
    story.append(Paragraph("Certifications", section_style))
    story.append(Paragraph("• AWS Certified Solutions Architect – Associate (2023)", bullet_style))
    story.append(Paragraph("• Google Professional Data Engineer (2022)", bullet_style))
    story.append(Paragraph("• Deep Learning Specialization — Coursera / Andrew Ng (2021)", bullet_style))

    doc.build(story)
    print(f"✅  Sample resume generated: {path}")
    return path


if __name__ == "__main__":
    generate()
