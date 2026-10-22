import unittest
import cafe_app

class CheckoutTests(unittest.TestCase):
    def setUp(self):
        cafe_app.app.config["TESTING"] = True
        self.client = cafe_app.app.test_client()
        cafe_app.users.clear()
        cafe_app.orders.clear()

        # Get a CSRF token.
        self.client.get("/login")
        with self.client.session_transaction() as session:
            self.csrf_token = session["_csrf_token"]

    def add_cart_item(self):
        return self.client.post(
            "/add_to_cart/1/1",
            data={
                "quantity": "1",
                "csrf_token": self.csrf_token,
            },
        )

    def create_and_login_user(self):
        response = self.client.post(
            "/register",
            data={
                "csrf_token": self.csrf_token,
                "name": "CheckoutTester",
                "email": "checkout@example.com",
                "phone": "0712345678",
                "password": "StrongPass123",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_checkout_redirects_when_cart_is_empty(self):
        self.create_and_login_user()

        response = self.client.get("/checkout")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/view_cart", response.location)

    def test_checkout_redirects_logged_out_user_with_items(self):
        self.add_cart_item()

        response = self.client.get("/checkout")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    def test_logged_in_user_can_open_checkout_with_items(self):
        self.create_and_login_user()
        self.add_cart_item()

        response = self.client.get("/checkout")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"checkout", response.data.lower())

    def test_logout_clears_login_session(self):
        self.create_and_login_user()

        response = self.client.get("/logout")

        self.assertEqual(response.status_code, 302)
        with self.client.session_transaction() as session:
            self.assertNotIn("user_email", session)

if __name__ == "__main__":
    unittest.main()
