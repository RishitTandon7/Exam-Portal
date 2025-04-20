from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)
users = []
# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="exam_portal"
)
cursor = conn.cursor(dictionary=True)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email.endswith("@student.com"):
            cursor.execute("SELECT * FROM Student WHERE Email=%s AND Password=%s", (email, password))
            user = cursor.fetchone()
            if user:
                return redirect(url_for('student_dashboard'))
            else:
                return "Invalid student credentials", 401

        elif email.endswith("@teacher.com"):
            cursor.execute("SELECT * FROM Faculty WHERE Email=%s AND Password=%s", (email, password))
            user = cursor.fetchone()
            if user:
                return redirect(url_for('teacher_dashboard'))
            else:
                return "Invalid teacher credentials", 401

        return "Invalid credentials", 400

    return render_template('login.html')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match!"

        try:
            print(f"Trying to register: {name}, {email}")

            if email.endswith("@student.com"):
                cursor.execute("INSERT INTO Student (Name, Email, Password) VALUES (%s, %s, %s)", (name, email, password))
            elif email.endswith("@teacher.com"):
                cursor.execute("INSERT INTO Faculty (Name, Email, Password) VALUES (%s, %s, %s)", (name, email, password))
            else:
                return "Invalid email domain. Use @student.com or @teacher.com"

            conn.commit()
            print("Registration successful, data committed.")
            return redirect(url_for('login'))

        except mysql.connector.Error as err:
            print("DB Error:", err)
            return f"Database error: {err}"

    return render_template('register.html')
@app.route('/create_exam', methods=['GET', 'POST'])
def create_exam():
    if request.method == 'POST':
        subject = request.form['subject']
        date = request.form['date']
        duration = request.form['duration']
        faculty_email = request.form['email']

        # Get Faculty_ID from email
        cursor.execute("SELECT Faculty_ID FROM Faculty WHERE Email=%s", (faculty_email,))
        result = cursor.fetchone()
        if not result:
            return "Invalid Faculty Email"
        faculty_id = result['Faculty_ID']

        cursor.execute("INSERT INTO Exam (Subject, Date, Duration, Faculty_ID) VALUES (%s, %s, %s, %s)",
                       (subject, date, duration, faculty_id))
        conn.commit()
        exam_id = cursor.lastrowid
        return redirect(url_for('add_questions', exam_id=exam_id))

    return render_template('create_exam.html')
@app.route('/add_questions/<int:exam_id>', methods=['GET', 'POST'])
def add_questions(exam_id):
    if request.method == 'POST':
        question_type = request.form['type']
        marks = request.form['marks']
        difficulty = request.form['difficulty']
        question_text = request.form['question']

        # Insert question
        cursor.execute("""
            INSERT INTO Question (Exam_ID, Type, Marks, Difficulty_Level)
            VALUES (%s, %s, %s, %s)
        """, (exam_id, question_type, marks, difficulty))
        conn.commit()
        question_id = cursor.lastrowid

        # Add options if MCQ or True/False
        if question_type in ['MCQ', 'True/False']:
            for i in range(1, 5):
                option_text = request.form.get(f'option_{i}')
                is_correct = request.form.get('correct') == str(i)
                if option_text:
                    cursor.execute("""
                        INSERT INTO Options (Question_ID, Option_Text, Is_Correct, Option_Order)
                        VALUES (%s, %s, %s, %s)
                    """, (question_id, option_text, is_correct, i))
        conn.commit()

        return redirect(url_for('add_questions', exam_id=exam_id))  # keep adding

    return render_template('add_questions.html', exam_id=exam_id)


@app.route('/teacher_dashboard')
def teacher_dashboard():
    return render_template('teacher_dashboard.html')

@app.route('/student_dashboard')
def student_dashboard():
    return render_template('student_dashboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)