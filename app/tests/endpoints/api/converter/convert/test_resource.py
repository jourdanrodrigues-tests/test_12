from pathlib import Path

from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase

TEST_DIR = settings.BASE_DIR / Path('app/test_files')


class TestPost(APITestCase):
    maxDiff = None

    def test_api_convert_empty_document(self):
        with (TEST_DIR / Path('empty.xml')).open() as xml_file:
            response = self.client.post('/api/converter/convert/', {'file': xml_file})

        self.assertListEqual(
            [response.status_code, response.json()],
            [status.HTTP_200_OK, {"Root": ""}],
        )