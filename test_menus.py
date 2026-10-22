import html
import unittest

import cafe_app


class MenuTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cafe_app.app.config["TESTING"] = True
        cls.client = cafe_app.app.test_client()

    def test_every_cafe_menu_loads_successfully(self):
        for cafe in cafe_app.cafes:
            with self.subTest(cafe=cafe["name"]):
                response = self.client.get(f"/menu/{cafe['id']}")
                page = html.unescape(response.get_data(as_text=True))

                self.assertEqual(response.status_code, 200)
                self.assertIn(cafe["name"], page)

    def test_unknown_cafe_menu_is_not_found(self):
        response = self.client.get("/menu/999999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
