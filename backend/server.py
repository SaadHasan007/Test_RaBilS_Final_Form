from dotenv import load_dotenv
load_dotenv()  # Loads OPENAI_API_KEY from backend/.env automatically

from flask import Flask, request, jsonify
from flask_cors import CORS
from modules.validator import check_ambiguity
from modules.prioritizer import calculate_priority
from modules.generator import generate_test_cases

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return "Backend is running! Please visit the frontend at <a href='http://localhost:5173'>http://localhost:5173</a>"


# ─────────────────────────────────────────────────────────────────────────────
# POST /api/ambiguity
# Body: { "user_story": str }
# Returns:
#   {
#     "formatted_story": str,   <- cleaned, reformatted user story
#     "ambiguity_notes": [str], <- list of issues detected / changes made
#     "used_ai": bool           <- whether GPT was used
#   }
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/api/ambiguity', methods=['POST'])
def check_ambiguity_route():
    data = request.json
    user_story = data.get('user_story', '')

    if not user_story:
        return jsonify({'error': 'User story is required'}), 400

    result = check_ambiguity(user_story)
    return jsonify(result)


# ─────────────────────────────────────────────────────────────────────────────
# POST /api/generate
# Body: { "user_story": str, "formatted_story": str (optional) }
#   - If "formatted_story" is provided (from the ambiguity check step), it is
#     used for generation instead of the raw user_story.
# Returns: { "gherkin": str, "priority": str }
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/api/generate', methods=['POST'])
def generate_route():
    data = request.json
    user_story = data.get('user_story', '')

    if not user_story:
        return jsonify({'error': 'User story is required'}), 400

    # Use the AI-formatted story for generation if it was provided by the
    # ambiguity check step; otherwise fall back to the raw input.
    story_for_generation = data.get('formatted_story') or user_story

    generated_gherkin = generate_test_cases(story_for_generation)
    priority = calculate_priority(generated_gherkin, story_for_generation)

    return jsonify({
        'gherkin': generated_gherkin,
        'priority': priority
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
