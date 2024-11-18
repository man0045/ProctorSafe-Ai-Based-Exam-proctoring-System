from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Serve the HTML file
@app.route('/')
def index():
    return render_template('index.html')  # Make sure 'index.html' is in a 'templates' folder

# Sample question generation logic
def generate_questions(text, num_questions, question_type):
    sentences = text.split('.')
    questions = []
    
    for _ in range(int(num_questions)):
        sentence = random.choice(sentences).strip()
        if question_type == 'objective':
            question = f"What is discussed in this sentence: \"{sentence}\"?"
        else:
            question = f"Explain the significance of: \"{sentence}\""
        questions.append(question)
    
    return questions

@app.route('/generate_questions', methods=['POST'])
def generate_questions_endpoint():
    data = request.get_json()
    input_text = data['text']
    num_questions = data['num_questions']
    question_type = data['question_type']

    questions = generate_questions(input_text, num_questions, question_type)
    return jsonify({"questions": questions})

if __name__ == '__main__':
    app.run(debug=True)
