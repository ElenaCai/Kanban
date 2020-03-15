import os
import unittest
import app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

TEST_DB = 'test.db'

class TestToDo(unittest.TestCase):
    # set up a temporary database
    def setUp(self):
        self.app = app.app.test_client()
        self.db = app.db

        self.db.drop_all()
        self.db.create_all()

        # Create some tasks
        self.task1 = "Imaginary Task 1"
        self.task2 = "Imaginary Task 2"
        self.task3 = "Imaginary Task 3"

    def tearDown(self):
        pass

    # Test entering the main page
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # Test new event creating
    def test_create_task(self):
        response = self.app.post('/add', data=dict(todoitem=self.task1), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
