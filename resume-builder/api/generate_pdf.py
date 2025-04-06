from flask import Flask, request, send_file, jsonify
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
import io
import json

app = Flask(__name__)

# Register a font (replace 'arial.ttf' with the actual path)
try:
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    baseFontName = 'Arial'
except FileNotFoundError:
    print("Warning: 'arial.ttf' not found. Using a default font.")
    baseFontName = 'Helvetica'

def generate_resume_pdf_bytes(resume_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            leftMargin=0.75*inch, rightMargin=0.75*inch,
                            topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    h1_style = styles['h1']
    h2_style = styles['h2']
    bold_style = ParagraphStyle(
        'BoldStyle',
        parent=normal_style,
        fontName=baseFontName,
        fontSize=10,
        leading=12,
        spaceAfter=6
    )
    section_title_style = ParagraphStyle(
        'SectionTitleStyle',
        parent=normal_style,
        fontName=baseFontName,
        fontSize=12,
        leading=14,
        spaceBefore=12,
        spaceAfter=6,
        textColor=colors.black
    )
    normal_style.fontName = baseFontName
    normal_style.fontSize = 10
    normal_style.leading = 12
    normal_style.spaceAfter = 6
    h1_style.fontName = baseFontName
    h1_style.fontSize = 18
    h1_style.leading = 20
    h2_style.fontName = baseFontName
    h2_style.fontSize = 14
    h2_style.leading = 16
    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=normal_style,
        fontName=baseFontName,
        fontSize=9,
        leading=10,
        textColor=colors.grey
    )

    story = []

    # Header
    story.append(Paragraph(resume_data.get('name', 'Your Name').upper(), h1_style))
    story.append(Paragraph(resume_data.get('degree', resume_data.get('jobTitle', 'Designation')), h2_style))
    contact_info = f"{resume_data.get('phone', 'Phone')} | {resume_data.get('email', 'Email')} | {resume_data.get('Address', 'Address')}"
    story.append(Paragraph(contact_info, contact_style))
    story.append(Spacer(1, 0.2*inch))

    # Objective
    if 'summary' in resume_data:
        story.append(Paragraph("OBJECTIVE", section_title_style))
        story.append(Paragraph(resume_data['summary'], normal_style))
        story.append(Spacer(1, 0.2*inch))

    # Experience
    if 'experience' in resume_data and isinstance(resume_data['experience'], list):
        story.append(Paragraph("EXPERIENCE", section_title_style))
        for exp in resume_data['experience']:
            title_company = f"<b>{exp.get('jobTitle', 'Job Title')}</b>, {exp.get('company', 'Company')}"
            years = f"({exp.get('expYears', 'Years')})"
            story.append(Paragraph(f"{title_company} <font size=9 color='grey'>{years}</font>", normal_style))
            story.append(Paragraph(exp.get('jobDescription', 'Description'), normal_style))
            story.append(Spacer(1, 0.1*inch))
        story.append(Spacer(1, 0.2*inch))

    # Education
    if 'education' in resume_data and isinstance(resume_data['education'], list):
        story.append(Paragraph("EDUCATION", section_title_style))
        for edu in resume_data['education']:
            degree_institution = f"<b>{edu.get('degree', 'Degree')}</b>, {edu.get('institution', 'Institution')}"
            year = f"({edu.get('eduYear', 'Year')})"
            story.append(Paragraph(f"{degree_institution} <font size=9 color='grey'>{year}</font>", normal_style))
            story.append(Spacer(1, 0.1*inch))
        story.append(Spacer(1, 0.2*inch))

    # Skills
    if 'skills' in resume_data:
        story.append(Paragraph("SKILLS", section_title_style))
        skills_list = [skill.strip() for skill in resume_data['skills'].split(',') if skill.strip()]
        data = [skills_list[i:i + 5] for i in range(0, len(skills_list), 5)]
        table = Table(data, colWidths=[(doc.width - 1.5*inch) / 5.0] * 5)
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), baseFontName),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('LEADING', (0, 0), (-1, -1), 12),
        ]))
        story.append(table)
        story.append(Spacer(1, 0.2*inch))

    doc.build(story)
    buffer.seek(0)
    return buffer

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    try:
        resume_data = request.get_json()
        if not resume_data:
            return jsonify({'error': 'No resume data received'}), 400

        pdf_buffer = generate_resume_pdf_bytes(resume_data)
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='resume.pdf'
        )
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)