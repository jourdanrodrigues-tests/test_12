from pathlib import Path

from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase

TEST_DIR = settings.BASE_DIR / Path('app/test_files')


class TestPost(APITestCase):
    maxDiff = None

    def test_connected_convert_empty_document(self):
        with (TEST_DIR / Path('empty.xml')).open() as xml_file:
            response = self.client.post('/connected/', {'file': xml_file})

        self.assertListEqual(
            [response.status_code, response.json()],
            [status.HTTP_200_OK, {"Root": ""}],
        )

    def test_connected_convert_addresses(self):
        with (TEST_DIR / Path('addresses.xml')).open() as xml_file:
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
