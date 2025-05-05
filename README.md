# Exam Portal

This is a web-based Exam Portal application built with Flask and MySQL. It supports student and faculty roles, allowing exam creation, question management, exam taking, and result viewing.

## Features

- User registration and login for students and faculty
- Exam creation and question addition by faculty
- Students can take exams and submit answers
- Result calculation and viewing for students and faculty
- Profile management and dashboards

## Technologies Used

- Python Flask
- MySQL
- HTML, CSS, JavaScript

## Setup Instructions

1. Install required Python packages:
   ```
   pip install flask flask-cors mysql-connector-python
   ```

2. Set up MySQL database and import schema from `exam_portal.sql`.

3. Run the Flask app:
   ```
   python app.py
   ```

4. Access the app at `http://localhost:5000`.

## License

This project is licensed under the MIT License.
