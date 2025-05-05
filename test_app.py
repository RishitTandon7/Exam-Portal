import unittest
from app import app

class ExamPortalTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_redirect(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_login_page(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_register_page(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_student_dashboard_redirect(self):
        response = self.app.get('/student_dashboard')
        self.assertEqual(response.status_code, 302)  # Redirect to login if not logged in

    def test_teacher_dashboard_redirect(self):
        response = self.app.get('/teacher_dashboard')
        self.assertEqual(response.status_code, 302)  # Redirect to login if not logged in

    def test_create_exam_page(self):
        response = self.app.get('/create_exam')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create New Exam', response.data)

    def test_login_post_invalid(self):
        response = self.app.post('/login', data=dict(email='invalid@example.com', password='wrong'))
        self.assertIn(response.status_code, [400, 401])

if __name__ == '__main__':
    unittest.main()
