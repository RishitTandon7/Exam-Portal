from flask_cors import CORS
from flask import Flask, request, render_template, redirect, url_for, jsonify, session
import mysql.connector
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'
CORS(app)
logging.basicConfig(level=logging.DEBUG)

# Flask app initialization and configuration
# Secret key is used for session management
# CORS enabled for cross-origin requests

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="exam_portal"
)
cursor = conn.cursor(dictionary=True)

questions_store = {}  # In-memory store for questions

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login for students and faculty.
    Validates email and password, sets session variables.
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email.endswith("@student.com"):
            cursor.execute("SELECT * FROM Student WHERE Email=%s AND Password=%s", (email, password))
            user = cursor.fetchone()
            if user:
                session['student_id'] = user['Student_ID']
                session['student_name'] = user['Name']
                return redirect(url_for('student_dashboard'))
            else:
                return "Invalid student credentials", 401

        elif email.endswith("@teacher.com"):
            cursor.execute("SELECT * FROM Faculty WHERE Email=%s AND Password=%s", (email, password))
            user = cursor.fetchone()
            if user:
                session['faculty_id'] = user['Faculty_ID']
                return redirect(url_for('teacher_dashboard'))
            else:
                return "Invalid teacher credentials", 401

        return "Invalid credentials", 400

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration for students and faculty.
    Validates input and inserts user into database.
    """
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        department_id = request.form.get('department')
        course_id = request.form.get('course')

        if password != confirm_password:
            return "Passwords do not match!"

        try:
            if email.endswith("@student.com"):
                cursor.execute("INSERT INTO Student (Name, Email, Password, Course_ID) VALUES (%s, %s, %s, %s)", (name, email, password, course_id))
            elif email.endswith("@teacher.com"):
                cursor.execute("INSERT INTO Faculty (Name, Email, Password, Dept_ID) VALUES (%s, %s, %s, %s)", (name, email, password, department_id))
            else:
                return "Invalid email domain. Use @student.com or @teacher.com"

            conn.commit()
            return redirect(url_for('login'))

        except mysql.connector.Error as err:
            return f"Database error: {err}"

    # GET request: fetch departments and courses
    cursor.execute("SELECT Dept_ID, Name FROM Department")
    departments = cursor.fetchall()
    cursor.execute("SELECT Course_ID, Name FROM Course")
    courses = cursor.fetchall()

    return render_template('register.html', departments=departments, courses=courses)


@app.route('/student_dashboard')
def student_dashboard():
    if 'student_id' not in session:
        return redirect(url_for('login'))
    return render_template('student_dashboard.html')

@app.route('/teacher_dashboard')
def teacher_dashboard():
    if 'faculty_id' not in session:
        return redirect(url_for('login'))
    return render_template('teacher_dashboard.html')

@app.route('/create_exam', methods=['GET', 'POST'])
def create_exam():
    if request.method == 'POST':
        subject = request.form['subject']
        date = request.form['date']
        duration = request.form['duration']
        faculty_email = request.form['email']

        cursor.execute("SELECT Faculty_ID FROM Faculty WHERE Email=%s", (faculty_email,))
        result = cursor.fetchone()
        if not result:
            return "Invalid Faculty Email"
        faculty_id = result['Faculty_ID']

        cursor.execute("INSERT INTO Exam (Subject, Date, Duration, Faculty_ID) VALUES (%s, %s, %s, %s)",
                       (subject, date, duration, faculty_id))
        conn.commit()
        exam_id = cursor.lastrowid
        # Redirect to add_questions to add questions to the exam
        return redirect(url_for('add_questions', exam_id=exam_id))

    return render_template('create_exam.html')

@app.route('/add_questions/<int:exam_id>', methods=['GET', 'POST'])
def add_questions(exam_id):
    if request.method == 'POST':
        question_type = request.form['type']
        marks = request.form['marks']
        difficulty = request.form['difficulty']
        question_text = request.form['question']
        correct_option = request.form.get('correct')

        # Generate unique question ID for in-memory store
        import uuid
        question_id = str(uuid.uuid4())

        # Save question in in-memory store with Question_ID
        question = {
            'Question_ID': question_id,
            'Type': question_type,
            'Marks': marks,
            'Difficulty_Level': difficulty,
            'Question_Text': question_text,
            'Options': []
        }

        if question_type in ['MCQ', 'True/False']:
            for i in range(1, 5):
                option_text = request.form.get(f'option_{i}')
                is_correct = (correct_option == str(i))
                if option_text and option_text.strip():
                    option_id = str(uuid.uuid4())
                    question['Options'].append({
                        'Option_ID': option_id,
                        'Option_Text': option_text.strip(),
                        'Is_Correct': is_correct,
                        'Option_Order': i
                    })

        if exam_id not in questions_store:
            questions_store[exam_id] = []
        questions_store[exam_id].append(question)

        return redirect(url_for('add_questions', exam_id=exam_id))

    return render_template('add_questions.html', exam_id=exam_id)

@app.route('/student_exams')
def student_exams():
    if 'student_id' not in session:
        return redirect(url_for('login'))

    student_id = session['student_id']
    cursor.execute("SELECT Course_ID FROM Student WHERE Student_ID = %s", (student_id,))
    student_course = cursor.fetchone()

    if not student_course or not student_course['Course_ID']:
        cursor.execute("SELECT Exam_ID, Subject, Date, Duration FROM Exam")
        exams = cursor.fetchall()
    else:
        course_id = student_course['Course_ID']
        cursor.execute("SELECT Faculty_ID FROM Course WHERE Course_ID = %s", (course_id,))
        faculty = cursor.fetchone()
        if not faculty or not faculty['Faculty_ID']:
            exams = []
        else:
            faculty_id = faculty['Faculty_ID']
            cursor.execute("SELECT Exam_ID, Subject, Date, Duration FROM Exam WHERE Faculty_ID = %s", (faculty_id,))
            exams = cursor.fetchall()

    return render_template('student_exams.html', exams=exams)

@app.route('/take_exam/<int:exam_id>', methods=['GET', 'POST'])
def take_exam(exam_id):
    if request.method == 'POST':
        # Clear previous answers for this student and exam to avoid duplicates
        if 'student_id' not in session:
            return "Student not logged in", 401
        student_id = session['student_id']

        cursor.execute("DELETE FROM Student_Answer WHERE Student_ID = %s AND Exam_ID = %s", (student_id, exam_id))
        conn.commit()

        answers = {}
        for key, value in request.form.items():
            if key.startswith('answer_'):
                question_id_str = key.split('_')[1]
                if not question_id_str.isdigit():
                    continue
                question_id = int(question_id_str)
                if value is None or value.strip() == '':
                    continue
                answers[question_id] = value

        for question_id, answer in answers.items():
            try:
                option_id = int(answer)
                cursor.execute("""
                    INSERT INTO Student_Answer (Student_ID, Exam_ID, Question_ID, Option_ID)
                    VALUES (%s, %s, %s, %s)
                """, (student_id, exam_id, question_id, option_id))
            except ValueError:
                cursor.execute("""
                    INSERT INTO Student_Answer (Student_ID, Exam_ID, Question_ID, Answer_Text)
                    VALUES (%s, %s, %s, %s)
                """, (student_id, exam_id, question_id, answer))
        conn.commit()

        # Fetch questions and options from database for scoring
        cursor.execute("""
            SELECT q.Question_ID, q.Type, q.Marks, q.Difficulty_Level,
                   o.Option_ID, o.Option_Text, o.Is_Correct, o.Option_Order
            FROM Question q
            LEFT JOIN Options o ON q.Question_ID = o.Question_ID
            WHERE q.Exam_ID = %s
            ORDER BY q.Question_ID, o.Option_Order
        """, (exam_id,))
        rows = cursor.fetchall()

        questions = {}
        for row in rows:
            qid = row['Question_ID']
            if qid not in questions:
                questions[qid] = {
                    'Question_ID': qid,
                    'Type': row['Type'],
                    'Marks': row['Marks'],
                    'Difficulty_Level': row['Difficulty_Level'],
                    'Question_Text': '',
                    'Options': []
                }
            if row['Option_ID']:
                questions[qid]['Options'].append({
                    'Option_ID': row['Option_ID'],
                    'Option_Text': row['Option_Text'],
                    'Is_Correct': row['Is_Correct'],
                    'Option_Order': row['Option_Order']
                })
        questions_list = list(questions.values())

        # Fetch student's answers
        cursor.execute("""
            SELECT Question_ID, Option_ID, Answer_Text FROM Student_Answer
            WHERE Student_ID = %s AND Exam_ID = %s
        """, (student_id, exam_id))
        student_answers = cursor.fetchall()
        student_answer_map = {}
        for sa in student_answers:
            student_answer_map[sa['Question_ID']] = sa

        import logging
        logging.debug(f"Questions list from DB for exam {exam_id}: {questions_list}")
        logging.debug(f"Student answers fetched from DB: {student_answers}")
        total_score = 0.0
        total_marks = 0.0

        # Prepare mapping of question_id to marks, correct options, and type for efficiency
        question_data_map = {}

        for q in questions_list:
            qid = q.get('Question_ID')
            if qid is None:
                continue
            try:
                marks = float(q.get('Marks', 0))
            except Exception as e:
                logging.error(f"Error converting marks to float for question {qid}: {e}")
                marks = 0.0

            correct_option_ids = set()
            for option in q.get('Options', []):
                if option.get('Is_Correct'):
                    correct_option_ids.add(option['Option_ID'])

            qtype = q.get('Type')

            question_data_map[qid] = {
                'marks': marks,
                'correct_options': correct_option_ids,
                'type': qtype
            }
            total_marks += marks

        # Calculate total score by comparing student answers with correct options
        for qid, sa in student_answer_map.items():
            qdata = question_data_map.get(qid)
            if not qdata:
                continue
            marks = qdata['marks']
            correct_options = qdata['correct_options']
            qtype = qdata['type']

            if qtype in ['MCQ', 'True/False']:
                if sa['Option_ID'] is not None and sa['Option_ID'] in correct_options:
                    total_score += marks
            else:
                # For other question types, compare answer text with correct answer text if available
                pass

        logging.debug(f"Total score calculated: {total_score}, Total marks: {total_marks}")

        cursor.execute("""
            SELECT Result_ID FROM Result WHERE Student_ID = %s AND Exam_ID = %s
        """, (student_id, exam_id))
        existing_result = cursor.fetchone()

        status = 'Pass' if total_score >= total_marks / 2 else 'Fail'

        if existing_result:
            cursor.execute("""
                UPDATE Result SET Score = %s, Status = %s WHERE Result_ID = %s
            """, (total_score, status, existing_result['Result_ID']))
        else:
            cursor.execute("""
                INSERT INTO Result (Student_ID, Exam_ID, Score, Status)
                VALUES (%s, %s, %s, %s)
            """, (student_id, exam_id, total_score, status))
        conn.commit()

        # Redirect to view results page after submission
        if 'student_id' in session:
            return redirect(url_for('view_results'))
        elif 'faculty_id' in session:
            return redirect(url_for('teacher_results'))
        else:
            return "User not logged in", 401


    cursor.execute("""
        SELECT q.Question_ID, q.Type, q.Marks, q.Difficulty_Level,
               o.Option_ID, o.Option_Text, o.Is_Correct, o.Option_Order
        FROM Question q
        LEFT JOIN Options o ON q.Question_ID = o.Question_ID
        WHERE q.Exam_ID = %s
        ORDER BY q.Question_ID, o.Option_Order
    """, (exam_id,))
    rows = cursor.fetchall()

    if not rows and exam_id in questions_store:
        questions_list = questions_store[exam_id]
    else:
        questions = {}
        for row in rows:
            qid = row['Question_ID']
            if qid not in questions:
                questions[qid] = {
                    'Question_ID': qid,
                    'Type': row['Type'],
                    'Marks': row['Marks'],
                    'Difficulty_Level': row['Difficulty_Level'],
                    'Question_Text': '',
                    'Options': []
                }
            if row['Option_ID']:
                questions[qid]['Options'].append({
                    'Option_ID': row['Option_ID'],
                    'Option_Text': row['Option_Text'],
                    'Is_Correct': row['Is_Correct'],
                    'Option_Order': row['Option_Order']
                })
        questions_list = list(questions.values())

    if not questions_list:
        return render_template('take_exam.html', exam_id=exam_id, questions=[], message="No questions found for this exam. Please contact your teacher.")

    return render_template('take_exam.html', exam_id=exam_id, questions=questions_list)

@app.route('/view_results')
def view_results():
    if 'student_id' not in session:
        return redirect(url_for('login'))

    student_id = session['student_id']
    cursor.execute("""
        SELECT r.Exam_ID, e.Subject, e.Date, r.Score, r.Status
        FROM Result r
        JOIN Exam e ON r.Exam_ID = e.Exam_ID
        WHERE r.Student_ID = %s
    """, (student_id,))
    results = cursor.fetchall()

    return render_template('view_results.html', results=results)

@app.route('/view_students')
def view_students():
    if 'faculty_id' not in session:
        return redirect(url_for('login'))

    cursor.execute("SELECT Student_ID, Name, Email FROM Student")
    students = cursor.fetchall()

    return render_template('view_students.html', students=students)

@app.route('/view_exams')
def view_exams():
    if 'faculty_id' not in session:
        return redirect(url_for('login'))

    cursor.execute("SELECT Exam_ID, Subject, Date, Duration FROM Exam")
    exams = cursor.fetchall()

    return render_template('view_exams.html', exams=exams)


@app.route('/teacher_results')
def teacher_results():
    if 'faculty_id' not in session:
        return redirect(url_for('login'))

    faculty_id = session['faculty_id']
    cursor.execute("""
        SELECT r.Exam_ID, e.Subject, e.Date, r.Score, r.Status, s.Name as Student_Name
        FROM Result r
        JOIN Exam e ON r.Exam_ID = e.Exam_ID
        JOIN Student s ON r.Student_ID = s.Student_ID
        WHERE e.Faculty_ID = %s
    """, (faculty_id,))
    results = cursor.fetchall()

    return render_template('student_results.html', results=results)

@app.route('/profile')
def profile():
    if 'student_id' not in session:
        return redirect(url_for('login'))
    student_id = session['student_id']
    cursor.execute("SELECT * FROM Student WHERE Student_ID = %s", (student_id,))
    user = cursor.fetchone()
    if not user:
        return "User not found", 404
    role = 'Student'
    return render_template('profile.html', user=user, role=role)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
