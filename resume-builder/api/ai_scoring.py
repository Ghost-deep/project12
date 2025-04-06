from flask import request, jsonify
import re

# Dummy keyword scoring – replace with ML logic later
IMPORTANT_KEYWORDS = [
    'python', 'flask', 'django', 'react', 'sql',
    'machine learning', 'api', 'docker', 'git'
]

def ai_score_resume():
    data = request.get_json()
    text = f"{data.get('summary', '')} {data.get('experience', '')} {data.get('skills', '')}".lower()

    score = 0
    found_keywords = []

    for keyword in IMPORTANT_KEYWORDS:
        if re.search(rf"\b{keyword}\b", text):
            score += 10
            found_keywords.append(keyword)

    score = min(score, 100)  # Cap at 100

    feedback = "Great job!" if score >= 70 else (
        "Try to include more technical keywords or specific tools."
    )

    return jsonify({
        "score": score,
        "keywords_found": found_keywords,
        "feedback": feedback
    })
