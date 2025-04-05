from flask import Flask
from flask_cors import CORS

# Import API functions
from api.ai_scoring import ai_score_resume
from api.generate_pdf import generate_pdf
from api.export_docx import export_docx

app = Flask(__name__)
CORS(app) 
app.add_url_rule(
    '/api/score',
    view_func=ai_score_resume,
    methods=['POST']
)

# PDF Generation Endpoint
app.add_url_rule(
    '/api/generate-pdf',
    view_func=generate_pdf,
    methods=['POST']
)

# DOCX Export Endpoint
app.add_url_rule(
    '/api/export-docx',
    view_func=export_docx,
    methods=['POST']
)

# ======================
# 🏁 Run Server
# ======================
if __name__ == '__main__':
    app.run(debug=True)
