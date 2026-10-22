import unittest
import cafe_app

class RegistrationTests(unittest.TestCase):
    def setUp(self):
        cafe_app.app.config["TESTING"] = True
        self.client = cafe_app.app.test_client()

        # Keep each test independent.
        cafe_app.users.clear()

        # Obtain a valid CSRF token from a page visit.
        self.client.get("/register")
        with self.client.session_transaction() as session:
            self.csrf_token = session["_csrf_token"]

    def register(self, data):
        data["csrf_token"] = self.csrf_token
        return self.client.post("/register", data=data)

    def valid_details(self):
        return {
            "name": "TestUser",
            "email": "testuser@example.com",
            "phone": "0712345678",
            "password": "StrongPass123",
        }

    def test_registration_succeeds_with_valid_details(self):
        response = self.register(self.valid_details())

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(cafe_app.users), 1)
        self.assertIn("password_hash", cafe_app.users[0])
        self.assertNotEqual(
            cafe_app.users[0]["password_hash"],
            "StrongPass123",
        )

    def test_registration_rejects_missing_phone(self):
        details = self.valid_details()
        details["phone"] = ""

        response = self.register(details)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(cafe_app.users), 0)

    def test_registration_rejects_short_password(self):
        details = self.valid_details()
        details["password"] = "short"

        response = self.register(details)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(cafe_app.users), 0)

    def test_registration_rejects_duplicate_email(self):
        self.register(self.valid_details())

        duplicate = self.valid_details()
        duplicate["name"] = "AnotherUser"

        response = self.register(duplicate)

        self.assertEqual(response.status_code, 409)
        self.assertEqual(len(cafe_app.users), 1)

if __name__ == "__main__":
    unittest.main()
