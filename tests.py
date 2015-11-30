import os
from server import app
import unittest
from model import db, connect_to_db, example_data_users
# import doctest

sid = os.environ.get('TWILIO_ACCOUNT_SID')
token = os.environ.get('TWILIO_AUTH_TOKEN')
number = os.environ.get('TWILIO_NUMBER')

class MyFlaskIntegrationTests(unittest.TestCase):
    """test integration with framework - ie flask"""
    def setUp(self):
        #set up fake test browser
        self.client = app.test_client()

        #connect to temporary database
        connect_to_db(app, "sqlite:///")

        #500 error in route will raise an error in test
        app.config['TESTING'] = True

        #create tables and add sample data
        db.create_all()
        example_data_users()


    def test_load_homepage(self):
        """test to see if the index page comes up"""
        result = self.client.get("/")
        self.assertIn("text/html", result.headers['Content-Type'])
        self.assertEqual(result.status_code, 200)

# def load_tests(loader, tests, ignore):
#     """Also run our doctests and file-based doctests.

#     This function name, ``load_tests``, is required.
#     """

#     tests.addTests(doctest.DocTestSuite(server))
#     tests.addTests(doctest.DocFileSuite("tests.txt"))
#     return tests

# class ProjectTests(unittest.TestCase):
#     def setUp(self):
#         print "connecting to db"
#         ##db only lasts as long as the test
#         connect_to_db(app, "sqlite3:///")
#         self.client = app.test_client()
#         self._add_movie()    #so fake data runs for every test

#     def tearDown(self):
#         # If test does real work, clean up after. 
#         # Or just never commit it in the first place.
#         print "doing my teardown"
#         Movie.query.filter_by(title="Mad Max".delete()
#         db.commit()


if __name__ == '__main__':
    # If called like a script, run our tests

    unittest.main()