import os

from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase

TEST_FILES_DIR = os.path.join(settings.BASE_DIR, "app", "tests", "mock_files")


class TestPost(APITestCase):
    maxDiff = None

    def test_when_file_is_not_sent_then_returns_expected_response(self):
        response = self.client.post("/api/converter/convert/")

        self.assertListEqual(
            [response.status_code, response.json()],
            [status.HTTP_400_BAD_REQUEST, {"file": ["No file was submitted."]}],
        )

    def test_when_file_is_an_empty_root_then_returns_expected_response(self):
        with open(os.path.join(TEST_FILES_DIR, "empty_root.xml"), "rb") as xml_file:
            response = self.client.post("/api/converter/convert/", {"file": xml_file})

        self.assertListEqual(
            [response.status_code, response.json()],
            [status.HTTP_200_OK, {"Root": ""}],
        )

    def test_when_file_is_empty_then_returns_expected_response(self):
        with open(os.path.join(TEST_FILES_DIR, "empty.xml"), "rb") as xml_file:
            response = self.client.post("/api/converter/convert/", {"file": xml_file})

        self.assertListEqual(
            [response.status_code, response.json()],
            [status.HTTP_400_BAD_REQUEST, {"file": ["The submitted file is empty."]}],
        )

    def test_when_file_is_not_xml_then_returns_expected_response(self):
        with open(os.path.join(TEST_FILES_DIR, "blank.pdf"), "rb") as not_xml_file:
            response = self.client.post("/api/converter/convert/", {"file": not_xml_file})

        self.assertListEqual(
            [response.status_code, response.json()],
            [status.HTTP_400_BAD_REQUEST, {"file": ["Invalid XML file."]}],
        )

    def test_when_xml_file_has_two_root_elements_then_returns_expected_response(self):
        with open(os.path.join(TEST_FILES_DIR, "two_roots.xml"), "rb") as two_roots_file:
            response = self.client.post("/api/converter/convert/", {"file": two_roots_file})

        self.assertListEqual(
            [response.status_code, response.json()],
            [status.HTTP_400_BAD_REQUEST, {"file": ["Invalid XML file."]}],
        )

    def test_that_it_returns_expected_response(self):
        with open(os.path.join(TEST_FILES_DIR, "addresses.xml"), "rb") as xml_file:
            response = self.client.post("/api/converter/convert/", {"file": xml_file})

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
