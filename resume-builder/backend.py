from flask import Flask, request, send_file, jsonify, send_from_directory
from flask_cors import CORS
from api.ai_scoring import ai_score_resume
from api.generate_pdf import generate_pdf as generate_pdf_api  # Rename to avoid conflict
from api.export_docx import export_docx

app = Flask(__name__, static_folder='.') # Serve static files from the root directory
CORS(app)

app.add_url_rule('/api/score', view_func=ai_score_resume, methods=['POST'])
app.add_url_rule('/api/generate-pdf', view_func=generate_pdf_api, methods=['POST'])
app.add_url_rule('/api/export-docx', view_func=export_docx, methods=['POST'])

# Serve static HTML files
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/builder.html')
def serve_builder():
    return send_from_directory('.', 'builder.html')

@app.route('/preview.html')
def serve_preview():
    return send_from_directory('.', 'preview.html')

# Serve static CSS files
@app.route('/static/css/<path:filename>')
def serve_static_css(filename):
    return send_from_directory('static/css', filename)

# Serve static assets (like logo.png)
@app.route('/static/assets/<path:filename>')
def serve_static_assets(filename):
    return send_from_directory('static/assets', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5500) # Run on port 5500 to match your error screenshot