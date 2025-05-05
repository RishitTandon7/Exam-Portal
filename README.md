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

## Contribution Guidelines

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Write clear, concise commit messages.
4. Ensure code is well-documented and tested.
5. Submit a pull request describing your changes.

Thank you for helping improve the Exam Portal!
