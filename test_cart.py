import unittest
import cafe_app

class CartTests(unittest.TestCase):
    def setUp(self):
        self.client = cafe_app.app.test_client()
        # Create a session CSRF token, just as a page visit would.
        self.client.get("/login")
        with self.client.session_transaction() as session:
            self.csrf_token = session["_csrf_token"]

    def post_with_csrf(self, url, data=None):
        data = data or {}
        data["csrf_token"] = self.csrf_token
        return self.client.post(url, data=data)

    def test_add_update_remove_products_and_totals(self):
        # Add 2 Coffees at R5 each.
        response = self.post_with_csrf(
    "/add_to_cart/1/1",
    data={"quantity": "2"},
)
        self.assertEqual(response.status_code, 302)
        # Add 3 Teas at R3 each.
        response = self.post_with_csrf(
    "/add_to_cart/1/2",
    data={"quantity": "3"},
)
        self.assertEqual(response.status_code, 302)
        # Total: (2 x R5) + (3 x R3) = R19.
        response = self.client.get("/view_cart")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Total: R19.00", response.data)
        # Update Coffee quantity from 2 to 4.
        response = self.post_with_csrf(
            "/update_cart",
            data={
                "cafe_id": "1",
                "item_id": "1",
                "quantity": "4",
                "action": "update",
            },
        )
        self.assertEqual(response.status_code, 302)

        # Total: (4 x R5) + (3 x R3) = R29.
        response = self.client.get("/view_cart")
        self.assertIn(b"Total: R29.00", response.data)

        # Remove Tea.
        response = self.post_with_csrf(
    "/update_cart",
    data={
        "cafe_id": "1",
        "item_id": "2",
        "action": "remove",
    },
)
        self.assertEqual(response.status_code, 302)
        # Only 4 Coffees remain: R20.
        response = self.client.get("/view_cart")
        self.assertIn(b"Total: R20.00", response.data)
        self.assertIn(b"Coffee", response.data)
        self.assertNotIn(b">Tea<", response.data)

    def test_rejects_invalid_quantities(self):
        # Adding zero items must be rejected.
        response = self.client.post(
            "/add_to_cart/1/1",
            data={"quantity": "0"},
        )
        self.assertEqual(response.status_code, 400)

        # Adding more than 99 items must be rejected.
        response = self.client.post(
            "/add_to_cart/1/1",
            data={"quantity": "100"},
        )
        self.assertEqual(response.status_code, 400)

        # Add one valid item before testing an update.
        self.client.post(
            "/add_to_cart/1/1",
            data={"quantity": "1"},
        )

        # Updating to zero must be rejected.
        response = self.client.post(
            "/update_cart",
            data={
                "cafe_id": "1",
                "item_id": "1",
                "quantity": "0",
                "action": "update",
            },
        )
        self.assertEqual(response.status_code, 400)

        # Updating to more than 99 must be rejected.
        response = self.client.post(
            "/update_cart",
            data={
                "cafe_id": "1",
                "item_id": "1",
                "quantity": "100",
                "action": "update",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_rejects_post_without_csrf_token(self):
        response = self.client.post(
            "/add_to_cart/1/1",
            data={"quantity": "1"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"CSRF", response.data)

    def test_rejects_invalid_csrf_token(self):
        response = self.client.post(
            "/add_to_cart/1/1",
            data={
                "quantity": "1",
                "csrf_token": "invalid-token",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"CSRF", response.data)

if __name__ == "__main__":
    unittest.main()