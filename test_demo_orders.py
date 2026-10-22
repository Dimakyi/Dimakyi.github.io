import unittest
import cafe_app

class DemoOrderTests(unittest.TestCase):
    def setUp(self):
        cafe_app.app.config["TESTING"] = True
        self.client = cafe_app.app.test_client()

        cafe_app.users.clear()
        cafe_app.orders.clear()

        self.original_demo_setting = (
            cafe_app.COFFEE_JOURNEY_DEMO_ENABLED
        )

        self.client.get("/login")
        with self.client.session_transaction() as session:
            self.csrf_token = session["_csrf_token"]

        cafe_app.users.append({
            "name": "DemoTester",
            "email": "demo@example.com",
            "phone": "0712345678",
            "password_hash": "test-hash",
        })

        with self.client.session_transaction() as session:
            session["user_email"] = "demo@example.com"

        cafe_app.orders.append({
            "id": "test-order-1",
            "user": "DemoTester",
            "user_email": "demo@example.com",
            "items": [],
            "total": 10,
            "status": "Confirmed",
            "payment_method": "Simulated Demo Payment",
            "payment_status": "Simulated successfully — no real money",
        })

    def tearDown(self):
        cafe_app.COFFEE_JOURNEY_DEMO_ENABLED = (
            self.original_demo_setting
        )
        cafe_app.users.clear()
        cafe_app.orders.clear()

    def post_with_csrf(self, order_id, token=None):
        return self.client.post(
            f"/demo/advance-order/{order_id}",
            data={
                "csrf_token": (
                    self.csrf_token if token is None else token
                )
            },
        )

    def test_demo_controls_are_disabled_by_default_setting(self):
        cafe_app.COFFEE_JOURNEY_DEMO_ENABLED = False

        response = self.post_with_csrf("test-order-1")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            cafe_app.orders[0]["status"],
            "Confirmed",
        )

    def test_demo_rejects_missing_csrf_token(self):
        cafe_app.COFFEE_JOURNEY_DEMO_ENABLED = True

        response = self.post_with_csrf("test-order-1", token="")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            cafe_app.orders[0]["status"],
            "Confirmed",
        )

    def test_demo_rejects_invalid_csrf_token(self):
        cafe_app.COFFEE_JOURNEY_DEMO_ENABLED = True

        response = self.post_with_csrf(
            "test-order-1",
            token="invalid-token",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            cafe_app.orders[0]["status"],
            "Confirmed",
        )

    def test_demo_advances_order_to_next_stage(self):
        cafe_app.COFFEE_JOURNEY_DEMO_ENABLED = True

        response = self.post_with_csrf("test-order-1")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            cafe_app.orders[0]["status"],
            "Brewing",
        )

    def test_demo_cannot_change_another_users_order(self):
        cafe_app.COFFEE_JOURNEY_DEMO_ENABLED = True

        cafe_app.orders[0]["user_email"] = "someone-else@example.com"

        response = self.post_with_csrf("test-order-1")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            cafe_app.orders[0]["status"],
            "Confirmed",
        )

if __name__ == "__main__":
    unittest.main()
