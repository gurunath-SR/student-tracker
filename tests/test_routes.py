import unittest
from app import app
from flask import session

class TestRoutes(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SECRET_KEY'] = 'test_secret'
        self.app = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_index_redirect(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/login' in response.location)

    def test_login_selection(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Student Performance Tracker', response.data)

    def test_teacher_login_page(self):
        response = self.app.get('/teacher/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Teacher Login', response.data)

    def test_student_login_page(self):
        response = self.app.get('/student/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Student Login', response.data)
        
    def test_update_student_route_redirect(self):
        # Should redirect if not logged in
        response = self.app.get('/teacher/student/1CR18CS001/update')
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
