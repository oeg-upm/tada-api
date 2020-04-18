# project/test_basic.py


import os
import unittest

import io
from app import app

file_source = "tests/aaabasketballplayers.csv"


class SubjectTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        # app.config['TESTING'] = True
        # app.config['WTF_CSRF_ENABLED'] = False
        # app.config['DEBUG'] = False
        self.app = app.test_client()

        self.assertEqual(app.debug, False)

    def test_subject(self):
        data = {
            'col_id': 0,
            'alpha': 0.9,
        }
        f = open(file_source)
        file_content = f.read()
        data['source'] = (io.BytesIO(file_content), 'test.csv')
        response = self.app.post('/subject', data=data, content_type='multipart/form-data',follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        entities = response.json['entities']
        self.assertEqual(entities[0],'http://dbpedia.org/ontology/BasketballPlayer')

    def test_subject_thing(self):
        data = {
            'col_id': 0,
            'alpha': 1.0,
        }
        f = open(file_source)
        file_content = f.read()
        data['source'] = (io.BytesIO(file_content), 'test.csv')
        response = self.app.post('/subject', data=data, content_type='multipart/form-data',follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        entities = response.json['entities']
        self.assertEqual(entities[0],'http://www.w3.org/2002/07/owl#Thing')


if __name__ == "__main__":
    unittest.main()