import os
import flaskfactory
import unittest
import tempfile

from flaskfactory import app
from models.store_model import StoreModel

class flaskfactoryTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.testing = True
        self.app = flaskfactory.app.test_client()
        # with app.app_context():
        #     app.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_fail(self):
        self.assertTrue(False)

    def test_pass(self):
        self.assertTrue(True)

    def test_init(self):
        store = StoreModel('StoreX', True, 1.1, 2.2)
        self.assertIsInstance(store, StoreModel)

    def test_key_lower_case(self):
        store = StoreModel('StoreX', True, 1.1, 2.2)
        self.assertEqual(store.name, store.name.lower())



if __name__ == '__main__':
    unittest.main()
