from unittest import TestCase

from starlette.testclient import TestClient

from main import app


class TestMain(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 400)

