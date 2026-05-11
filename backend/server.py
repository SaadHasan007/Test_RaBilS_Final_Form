from dotenv import load_dotenv
load_dotenv()  # Loads OPENAI_API_KEY from backend/.env automatically

from flask import Flask, request, jsonify
from flask_cors import CORS
from modules.ambiguityRemover import check_ambiguity
from modules.prioritizer import calculate_priority
from modules.generator import generate_ac
from modules.nlp import nlp_processor, reset_ids
from modules.dublicateRemover import detect_dublicates
from modules.validator import generate_final_ambiguity_report

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

test_case_list = []
ambiguity_report = []
user_story_list = []

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


@app.route('/api/xAmbiguityReport', methods=['POST'])
def get_ambiguity_report_route():
    data = request.json
    user_story = data.get('user_story', '')

    if not user_story:
        return jsonify({'error': 'User story is required'}), 400

    result = generate_final_ambiguity_report(user_story,user_story_list)
    ambiguity_report.append(jsonify(result))
    print(jsonify(result))
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
        return jsonify({'error': 'User story is required (server.py ~56)'}), 400
    
    user_story_list.append(data.get('formatted_story') or user_story)
    # Use the AI-formatted story for generation if it was provided by the
    # ambiguity check step; otherwise fall back to the raw input.
    story_for_generation = data.get('formatted_story') or user_story


    acceptance_criteria = generate_ac(story_for_generation)

    #handle this error , this is due to priorty previusely takes string, but now we giving it a list
    #priority = calculate_priority(generated_gherkin, story_for_generation) 
    priority = calculate_priority(story_for_generation)

    generated_test_cases = nlp_processor(story_for_generation,acceptance_criteria,priority)
    test_case_list.append(generated_test_cases)
    return jsonify({
        'testcase': generated_test_cases,
    })

@app.route('/api/testcase_list', methods=['GET'])
def testcase_route():
    result = test_case_list
    return jsonify(result)

@app.route('/api/testcase_list', methods=['DELETE'])
def clear_testcase():
    reset_ids()
    global test_case_list
    test_case_list = []
    return jsonify({
        "message": "Test case list cleared"
    }), 200

@app.route('/api/dublicates',methods=['POST'])
def identify_dublicates_route():
    data = request.json
    user_story = data.get('user_story', '')

    if not user_story:
        return jsonify({'error': 'User story is required (server.py ~56)'}), 400

    result = detect_dublicates(user_story,test_case_list)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
