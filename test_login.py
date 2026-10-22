import unittest
import cafe_app

class LoginTests(unittest.TestCase):
    def setUp(self):
        cafe_app.app.config["TESTING"] = True
        self.client = cafe_app.app.test_client()
        cafe_app.users.clear()

        # Create a test account using the real registration route.
        self.client.get("/register")
        with self.client.session_transaction() as session:
            self.csrf_token = session["_csrf_token"]

        response = self.client.post(
            "/register",
            data={
                "csrf_token": self.csrf_token,
                "name": "LoginTester",
                "email": "logintester@example.com",
                "phone": "0712345678",
                "password": "StrongPass123",
            },
        )
        self.assertEqual(response.status_code, 302)

        # Log out so each login test starts signed out.
        self.client.get("/logout")

    def login(self, username, password):
        return self.client.post(
            "/login",
            data={
                "csrf_token": self.csrf_token,
                "login": username,
                "password": password,
            },
        )

    def test_login_with_email_succeeds(self):
        response = self.login(
            "logintester@example.com",
            "StrongPass123",
        )
        self.assertEqual(response.status_code, 302)

        with self.client.session_transaction() as session:
            self.assertEqual(
                session.get("user_email"),
                "logintester@example.com",
            )

    def test_login_with_username_succeeds(self):
        response = self.login("LoginTester", "StrongPass123")
        self.assertEqual(response.status_code, 302)

    def test_login_rejects_wrong_password(self):
        response = self.login(
            "logintester@example.com",
            "WrongPassword",
        )
        self.assertEqual(response.status_code, 401)

    def test_login_rejects_unknown_user(self):
        response = self.login(
            "unknown@example.com",
            "StrongPass123",
        )
        self.assertEqual(response.status_code, 401)

if __name__ == "__main__":
    unittest.main()