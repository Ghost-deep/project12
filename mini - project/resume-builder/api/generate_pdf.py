from flask import request, send_file, jsonify
from weasyprint import HTML
import os
import tempfile

def generate_pdf():
    data = request.get_json()
    html_content = data.get("html", "")

    if not html_content:
        return jsonify({"error": "No HTML content provided."}), 400

    try:
        # Create temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            HTML(string=html_content).write_pdf(tmp.name)
            tmp.flush()
            return send_file(tmp.name, as_attachment=True, download_name="resume.pdf")

    except Exception as e:
        return jsonify({"error": str(e)}), 500
