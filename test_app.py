import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app, jsonify
from models import setup_db, Car, Document

class JACHomeTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "jac_home_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_post_car_admin(self):
        res = self.client().post('/cars', 
        json={'name': 'Sei4', 'image_url': 'https://imageurl.com', 'endpoint': '/sei4'}, headers={"Authorization": "Bearer {}".format(os.environ.get('ADMIN_TOKEN'))})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_car'])

    def test_post_car_user(self):
        res = self.client().post('/cars', 
        json={'name': 'Sei4', 'image_url': 'https://imageurl.com', 'endpoint': '/sei4'}, headers={"Authorization": "Bearer {}".format(os.environ.get('USER_TOKEN'))})

        self.assertEqual(res.status_code, 401)

    def test_get_cars(self):
        res = self.client().get('/cars', headers={"Authorization": "Bearer {}".format(os.environ.get('ADMIN_TOKEN'))})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])

    def test_get_cars_existing_id(self):
        res = self.client().get('/cars/4', headers={"Authorization": "Bearer {}".format(os.environ.get('ADMIN_TOKEN'))})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])

    def test_get_cars_non_existing_id(self):
        res = self.client().get('/cars/99', headers={"Authorization": "Bearer {}".format(os.environ.get('ADMIN_TOKEN'))})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_delete_cars_admin(self):
        res = self.client().delete('/cars/13', headers={"Authorization": "Bearer {}".format(os.environ.get('ADMIN_TOKEN'))})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_cars_user(self):
        res = self.client().delete('/cars/13', headers={"Authorization": "Bearer {}".format(os.environ.get('USER_TOKEN'))})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_post_documents_admin(self):
        res = self.client().post('/documents', json={"car_id": 2, "doc_type": "JPG", "image_url": "https://11.com", "name": "PDF", "url": "https://11.com"}, headers={"Authorization": "Bearer {}".format(os.environ.get('ADMIN_TOKEN'))})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_documents_user(self):
        res = self.client().post('/documents', json={"car_id": 2, "doc_type": "JPG", "image_url": "https://11.com", "name": "PDF", "url": "https://11.com"}, headers={"Authorization": "Bearer {}".format(os.environ.get('USER_TOKEN'))})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_get_documents(self):
        res = self.client().get('/documents', headers={"Authorization": "Bearer {}".format(os.environ.get('ADMIN_TOKEN'))})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_documents_non_existing(self):
        res = self.client().get('/documents/99', headers={"Authorization": "Bearer {}".format(os.environ.get('ADMIN_TOKEN'))})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_patch_documents_admin(self):
        res = self.client().patch('/documents/14', json={"car_id": 2, "doc_type": "PNG", "image_url": "https://png.com", "name": "PDF", "url": "https://11.com"}, headers={"Authorization": "Bearer {}".format(os.environ.get('ADMIN_TOKEN'))})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_documents_user(self):
        res = self.client().patch('/documents/14', json={"car_id": 2, "doc_type": "PNG", "image_url": "https://png.com", "name": "PDF", "url": "https://11.com"}, headers={"Authorization": "Bearer {}".format(os.environ.get('USER_TOKEN'))})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_document_admin(self):
        res = self.client().delete('/documents/13', headers={"Authorization": "Bearer {}".format(os.environ.get('ADMIN_TOKEN'))})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_document_user(self):
        res = self.client().delete('/documents/13', headers={"Authorization": "Bearer {}".format(os.environ.get('USER_TOKEN'))})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_get_car_documents(self):
        res = self.client().get('/cars/2/documents', headers={"Authorization": "Bearer {}".format(os.environ.get('ADMIN_TOKEN'))})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_car_documents_no_auth(self):
        res = self.client().get('/cars/2/documents')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
