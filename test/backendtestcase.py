import unittest

from app import app, db


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.test_client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
