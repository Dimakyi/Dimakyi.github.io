import unittest
import cafe_app

class OrderTests(unittest.TestCase):
    def setUp(self):
        cafe_app.app.config["TESTING"] = True
        self.client = cafe_app.app.test_client()

        cafe_app.users.clear()
        cafe_app.orders.clear()

        self.client.get("/login")
        with self.client.session_transaction() as session:
            self.csrf_token = session["_csrf_token"]

    def post_with_csrf(self, url, data=None):
        data = dict(data or {})
        data["csrf_token"] = self.csrf_token
        return self.client.post(url, data=data)

    def register_and_login(self, name, email):
        response = self.post_with_csrf(
            "/register",
            {
                "name": name,
                "email": email,
                "phone": "0712345678",
                "password": "StrongPass123",
            },
        )
        self.assertEqual(response.status_code, 302)

    def add_cart_item(self):
        response = self.post_with_csrf(
            "/add_to_cart/1/1",
            {"quantity": "2"},
        )
        self.assertEqual(response.status_code, 302)

    def test_payment_creates_order_and_clears_cart(self):
        self.register_and_login("OrderTester", "orders@example.com")
        self.add_cart_item()

        response = self.post_with_csrf("/simulate_payment")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/order_history", response.location)
        self.assertEqual(len(cafe_app.orders), 1)

        order = cafe_app.orders[0]
        self.assertEqual(order["user_email"], "orders@example.com")
        self.assertEqual(order["status"], "Confirmed")
        self.assertEqual(order["payment_method"], "Simulated Demo Payment")
        self.assertIn("no real money", order["payment_status"])
        self.assertEqual(order["total"], 10)

        with self.client.session_transaction() as session:
            self.assertFalse(session.get("cart"))

    def test_payment_rejects_empty_cart(self):
        self.register_and_login("OrderTester", "orders@example.com")

        response = self.post_with_csrf("/simulate_payment")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/view_cart", response.location)
        self.assertEqual(cafe_app.orders, [])

    def test_payment_requires_login(self):
        self.add_cart_item()

        response = self.post_with_csrf("/simulate_payment")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)
        self.assertEqual(cafe_app.orders, [])

    def test_order_history_shows_only_current_users_orders(self):
        self.register_and_login("FirstUser", "first@example.com")
        self.add_cart_item()
        self.post_with_csrf("/simulate_payment")

        self.client.get("/logout")

        self.client.get("/login")
        with self.client.session_transaction() as session:
            self.csrf_token = session["_csrf_token"]

        self.register_and_login("SecondUser", "second@example.com")

        response = self.client.get("/order_history")

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"first@example.com", response.data)
        self.assertNotIn(b"OrderTester", response.data)
        self.assertNotIn(b"FirstUser", response.data)

    def test_order_history_requires_login(self):
        response = self.client.get("/order_history")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

if __name__ == "__main__":
    unittest.main()
