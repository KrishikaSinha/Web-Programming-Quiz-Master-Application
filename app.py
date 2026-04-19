from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "secret123"

questions = [
    {"q": "Capital of India?", "options": ["Delhi", "Mumbai", "Chennai", "Kolkata"], "answer": "Delhi"},
    {"q": "2 + 2 = ?", "options": ["3", "4", "5", "6"], "answer": "4"},
    {"q": "HTML stands for?", "options": ["Hyper Text Markup Language", "High Tech Modern Language", "Hyper Tool Multi Language", "None"], "answer": "Hyper Text Markup Language"},
    {"q": "Python is?", "options": ["Snake", "Programming Language", "Game", "Browser"], "answer": "Programming Language"},
    {"q": "CSS used for?", "options": ["Structure", "Styling", "Database", "Logic"], "answer": "Styling"}
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    shuffled = questions.copy()
    random.shuffle(shuffled)

    session['questions'] = shuffled   # ✅ store in session
    return render_template('quiz.html', questions=shuffled)

@app.route('/result', methods=['POST'])
def result():
    score = 0
    quiz_questions = session.get('questions')  # ✅ get same order

    for i in range(len(quiz_questions)):
        user_ans = request.form.get(f"q{i}")

        if user_ans == quiz_questions[i]["answer"]:
            score += 1
        elif user_ans:
            score -= 0.5

    if score < 0:
        score = 0

    if score == 5:
        feedback = "Excellent! 🎉"
    elif score >= 3:
        feedback = "Good Job 👍"
    else:
        feedback = "Try Again 😅"

    return render_template('result.html', score=score, total=5, feedback=feedback)

if __name__ == '__main__':
    app.run(debug=True)