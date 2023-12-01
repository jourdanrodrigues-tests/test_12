import os

from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase

TEST_FILES_DIR = os.path.join(settings.BASE_DIR, 'app', 'test_files')


class TestPost(APITestCase):
    maxDiff = None

    def test_when_file_is_not_xml_then_returns_expected_response(self):
        response = self.client.post('/connected/')

        # This is an HTML response, so regardless of an error or success, it'll return 200 with the content to be
        # displayed to the user.
        content = response.content.decode()
        self.assertIn('This field is required.', content)

    def test_when_file_is_empty_then_returns_expected_response(self):
        with open(os.path.join(TEST_FILES_DIR, 'empty.xml'), 'rb') as xml_file:
            response = self.client.post('/connected/', {'file': xml_file})

        self.assertListEqual(
            [response.status_code, response.json()],
            [status.HTTP_200_OK, {"Root": ""}],
        )

    def test_that_it_returns_expected_response(self):
        with open(os.path.join(TEST_FILES_DIR, 'addresses.xml'), 'rb') as xml_file:
            response = self.client.post('/connected/', {'file': xml_file})

        expected_data = {
            "Root": [
                {
                    "Address": [
                        {"StreetLine1": "123 Main St."},
                        {"StreetLine2": "Suite 400"},
                        {"City": "San Francisco"},
                        {"State": "CA"},
                        {"PostCode": "94103"},
                    ]
                },
                {
                    "Address": [
                        {"StreetLine1": "400 Market St."},
                        {"City": "San Francisco"},
                        {"State": "CA"},
                        {"PostCode": "94108"},
                    ]
                },
            ],
        }
        self.assertListEqual(
            [response.status_code, response.json()],
            [status.HTTP_200_OK, expected_data],
        )