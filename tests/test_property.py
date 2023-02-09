# project/test_basic.py
import os
import unittest

import io
import app as appmod

appmod.SOURCES_DIR = None

from app import app

file_source = "tests/test6.csv"
file_source1 = "tests/test1.csv"

class PropertyTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def test_property(self):
        """
        Property test
        """
        class_uri = "http://dbpedia.org/ontology/BaseballPlayer"
        data = {
            'subject_col_id': 2,
            'alpha': 0.9,
            'ann_source': 'test',
            'class_uri': class_uri
        }
        f = open(file_source1)
        file_content = f.read()
        f.close()
        file_content = file_content.encode('utf-8')
        data['source'] = (io.BytesIO(file_content), 'test.csv')
        response = self.app.post('/property', data=data, content_type='multipart/form-data',
                                 follow_redirects=True)
        print("Response: ")
        print(response)
        print(response.data)
        self.assertEqual(response.status_code, 200)
        # print(response.json)
        properties = response.json['cols_properties']
        self.assertGreater(len(properties), 0)


if __name__ == "__main__":
    unittest.main()
