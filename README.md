
# 📝 Exam Portal - Flask Web Application

A web-based Exam Portal built with **Flask** and **MySQL**, allowing students and teachers to register, login, and manage exams. Teachers can create exams and add questions, while students can view their dashboard after login.

---

## 🚀 Features

- 🔐 Secure login system for Students and Teachers
- 📚 Role-based dashboards (`/student_dashboard` and `/teacher_dashboard`)
- 📝 Teachers can create exams and add questions
- ❓ Support for MCQ and True/False questions
- ✅ Password confirmation during registration
- 🌐 Flask-CORS for frontend/backend integration
- 📡 Can be accessed on mobile through local IP

---

## 🧰 Tech Stack

| Component     | Technology          |
|---------------|---------------------|
| Backend       | Python (Flask)      |
| Frontend      | HTML (Flask templates) |
| Database      | MySQL               |
| Integration   | Flask-CORS          |

---

## 📁 Project Structure

```
exam-portal/
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── teacher_dashboard.html
│   ├── student_dashboard.html
│   ├── create_exam.html
│   └── add_questions.html
│
├── static/               # Optional - CSS, JS, images
├── app.py                # Main Flask application
└── README.md
```

---

## ⚙️ Installation

### 🔽 1. Clone the Repository

```bash
git clone https://github.com/your-username/exam-portal.git
cd exam-portal
```

### 📦 2. Install Required Packages

```bash
pip install flask flask-cors mysql-connector-python
```

### 🧱 3. Set Up MySQL Database

- Create a MySQL database named `exam_portal`

```

### ⚙️ 4. Configure MySQL in `app.py`

```python
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="exam_portal"
)
```

---

## 📲 Accessing on Your Phone (Local Network Hosting)

### ✅ Update this in your `app.py`:

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### 📱 Steps:

1. Run the app: `python app.py`
2. Get your computer’s local IP:
   - Windows: `ipconfig` → IPv4 address
   - Mac/Linux: `ifconfig`
3. On your phone (connected to same Wi-Fi), open browser and go to:

```
http://<your-local-ip>:5000
```

Example:
```
http:<your ip>:<your port number>
```

---

## 💡 Future Enhancements

- Student Exam Attempt Portal
- Results & Marks Dashboard
- Admin Panel
- Dockerization
- Hosting on Render/Heroku

---

## 👨‍💻 Developed By

**Rishit Tandon**  
🌐 [LinkedIn](https://www.linkedin.com/in/rishit-tandon)  
📧 rishit.tandon.7@gmail.com
