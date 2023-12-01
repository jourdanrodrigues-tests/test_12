import json
import os
import re

from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase

TEST_FILES_DIR = os.path.join(settings.BASE_DIR, "app", "tests", "mock_files")


def get_json_from_response(response) -> str | None:
    content = response.content.decode()
    match = re.search(r"<pre>((.|\s)+)</pre>", content)
    if not match:
        return None
    return json.loads(match.groups()[0].strip("'").strip('"'))


class TestGet(APITestCase):
    def test_that_it_returns_expected_status_code(self):
        response = self.client.post("/connected/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPost(APITestCase):
    maxDiff = None

    def test_when_file_is_not_xml_then_returns_expected_message(self):
        response = self.client.post("/connected/")

        # This is an HTML response, so regardless of an error or success, it'll return 200 with the content to be
        # displayed to the user.
        content = response.content.decode()
        self.assertIn("This field is required.", content)

    def test_when_file_is_empty_then_returns_expected_json_content(self):
        with open(os.path.join(TEST_FILES_DIR, "empty.xml"), "rb") as xml_file:
            response = self.client.post("/connected/", {"file": xml_file})

        self.assertListEqual(
            [response.status_code, get_json_from_response(response)],
            [status.HTTP_200_OK, {"Root": ""}],
        )

    def test_when_file_is_not_xml_then_returns_expected_error_message(self):
        with open(os.path.join(TEST_FILES_DIR, "blank.pdf"), "rb") as not_xml_file:
            response = self.client.post("/connected/", {"file": not_xml_file})

        self.assertIn("Invalid XML file.", response.content.decode())

    def test_when_xml_file_has_two_roots_then_returns_expected_error_message(self):
        with open(os.path.join(TEST_FILES_DIR, "two_roots.xml"), "rb") as two_roots_file:
            response = self.client.post("/connected/", {"file": two_roots_file})

        self.assertIn("Invalid XML file.", response.content.decode())

    def test_that_it_returns_expected_json_content(self):
        with open(os.path.join(TEST_FILES_DIR, "addresses.xml"), "rb") as xml_file:
            response = self.client.post("/connected/", {"file": xml_file})

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
            [response.status_code, get_json_from_response(response)],
            [status.HTTP_200_OK, expected_data],
        )
