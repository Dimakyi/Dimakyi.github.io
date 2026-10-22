import os
import uuid
import secrets

def get_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_urlsafe(32)
    return session['_csrf_token']

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY")
if not app.config["SECRET_KEY"]:
    raise RuntimeError("FLASK_SECRET_KEY environment variable must be set.")

@app.context_processor
def inject_csrf_token():
    return {"csrf_token": get_csrf_token()}

@app.before_request
def protect_post_requests():
    if request.method != "POST":
        return None

    submitted_token = request.form.get("csrf_token", "")
    session_token = session.get("_csrf_token", "")

    if not session_token or not secrets.compare_digest(
        submitted_token, session_token
    ):
        return "Invalid or missing CSRF token.", 400

    return None

# Local-only Coffee Journey demo control.
# Keep disabled unless you are running a trusted local demo.
COFFEE_JOURNEY_DEMO_ENABLED = (
    os.environ.get("COFFEE_JOURNEY_DEMO_ENABLED") == "1"
)

cafes = [
    {
        "id": 1,
        "name": "Mpho's Daily Grind",
        "menu": [
            {"id": 1, "item": "Coffee", "price": 5.0},
            {"id": 2, "item": "Tea", "price": 3.0},
        ],
    },
    {
        "id": 2,
        "name": "Thandi's Brew Corner",
        "menu": [
            {"id": 1, "item": "Latte", "price": 6.0},
            {"id": 2, "item": "Espresso", "price": 4.0},
        ],
    },
    {
        "id": 3,
        "name": "Jabu's Coffee House",
        "menu": [
            {"id": 1, "item": "Mocha", "price": 8.0},
            {"id": 2, "item": "Cappuccino", "price": 5.0},
        ],
    },
    {
        "id": 4,
        "name": "Lerato's Coffee Garden",
        "menu": [
            {"id": 1, "item": "Flat White", "price": 7.0},
            {"id": 2, "item": "Rooibos Tea", "price": 4.0},
        ],
    },
    {
        "id": 5,
        "name": "Soweto Sunrise Cafe",
        "menu": [
            {"id": 1, "item": "Cafe Mocha", "price": 8.0},
            {"id": 2, "item": "Hot Chocolate", "price": 6.0},
        ],
    },
    {
        "id": 6,
        "name": "Ubuntu Bean House",
        "menu": [
            {"id": 1, "item": "Americano", "price": 5.0},
            {"id": 2, "item": "Cappuccino", "price": 7.0},
        ],
    },
]

users = []
orders = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')

        if not name or not email or not phone or len(password) < 8:
            return "Please complete all fields and use a password of at least 8 characters.", 400

        if any(user['email'] == email for user in users):
            return "An account with this email already exists.", 409

        user = {
            "name": name,
            "email": email,
            "phone": phone,
            "password_hash": generate_password_hash(password)
        }
        users.append(user)
        session['user_email'] = email
        return redirect(url_for('browse_cafes'))

    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_value = request.form.get('login', '').strip()
        password = request.form.get('password', '')

        user = next(
            (
                u for u in users
                if u['email'] == login_value.lower()
                or u['name'].lower() == login_value.lower()
            ),
            None
        )

        if user and check_password_hash(user['password_hash'], password):
            session['user_email'] = user['email']
            return redirect(url_for('index'))

        return "Invalid username/email or password.", 401

    return render_template('login.html')

@app.route('/browse_cafes')
def browse_cafes():
    return render_template('browse_cafes.html', cafes=cafes)

@app.route('/menu/<int:cafe_id>')
def view_menu(cafe_id):
    cafe = next((c for c in cafes if c['id'] == cafe_id), None)

    if cafe is None:
        return "Cafe not found.", 404

    return render_template('menu.html', cafe=cafe)



def normalize_cart(cart):
    """Merge duplicate products and support older cart entries."""
    merged = {}

    for item in cart:
        key = (item["cafe_id"], item["item_id"])
        quantity = max(1, int(item.get("quantity", 1)))

        if key in merged:
            merged[key]["quantity"] += quantity
        else:
            merged[key] = {**item, "quantity": quantity}

    return list(merged.values())


@app.route('/add_to_cart/<int:cafe_id>/<int:item_id>', methods=['POST'])
def add_to_cart(cafe_id, item_id):
    cafe = next((c for c in cafes if c["id"] == cafe_id), None)

    if cafe is None:
        return "Cafe not found.", 404

    item = next((i for i in cafe["menu"] if i["id"] == item_id), None)

    if item is None:
        return "Item not found.", 404

    cart = normalize_cart(session.get("cart", []))
    quantity = request.form.get("quantity", default=1, type=int)

    if quantity is None or not 1 <= quantity <= 99:
        return "Quantity must be between 1 and 99.", 400

    existing = next(
        (
            entry for entry in cart
            if entry["cafe_id"] == cafe_id
            and entry["item_id"] == item_id
        ),
        None,
    )

    if existing:
        if existing["quantity"] + quantity > 99:
            return "Maximum quantity per product is 99.", 400
        existing["quantity"] += quantity
    else:
        cart.append({
            "cafe_id": cafe_id,
            "cafe_name": cafe["name"],
            "item_id": item["id"],
            "item": item["item"],
            "price": item["price"],
            "quantity": quantity,
        })

    session["cart"] = cart
    return redirect(url_for("view_cart"))


@app.route('/update_cart', methods=['POST'])
def update_cart():
    cart = normalize_cart(session.get("cart", []))
    cafe_id = request.form.get("cafe_id", type=int)
    item_id = request.form.get("item_id", type=int)
    action = request.form.get("action", "")
    entry = next(
        (
            item for item in cart
            if item["cafe_id"] == cafe_id
            and item["item_id"] == item_id
        ),
        None,
    )

    if entry is None:
        return redirect(url_for("view_cart"))

    if action == "remove":
        cart = [
            item for item in cart
            if not (
                item["cafe_id"] == cafe_id
                and item["item_id"] == item_id
            )
        ]
    elif action == "update":
        quantity = request.form.get("quantity", type=int)

        if quantity is None or not 1 <= quantity <= 99:
            return "Quantity must be between 1 and 99.", 400

        entry["quantity"] = quantity
    else:
        return "Invalid cart action.", 400

    session["cart"] = cart
    return redirect(url_for("view_cart"))


@app.route('/view_cart')
def view_cart():
    cart = normalize_cart(session.get("cart", []))
    session["cart"] = cart
    total = sum(item["price"] * item["quantity"] for item in cart)

    return render_template("cart.html", cart=cart, total=total)


@app.route('/checkout')
def checkout():
    cart = normalize_cart(session.get('cart', []))
    session['cart'] = cart

    if not cart:
        return redirect(url_for('view_cart'))

    user_email = session.get('user_email')

    if not user_email:
        return redirect(url_for('login'))

    user = next(
        (u for u in users if u['email'] == user_email),
        None
    )

    if user is None:
        session.pop('user_email', None)
        return redirect(url_for('login'))

    total = sum(
    item['price'] * item['quantity']
    for item in cart
)

    return render_template(
        'checkout.html',
        cart=cart,
        total=total
    )

@app.route('/place_order', methods=['POST'])
def place_order():
    return redirect(url_for('checkout'))


@app.route('/simulate_payment', methods=['POST'])
def simulate_payment():
    cart = normalize_cart(session.get('cart', []))
    session['cart'] = cart

    if not cart:
        return redirect(url_for('view_cart'))

    user_email = session.get('user_email')

    if not user_email:
        return redirect(url_for('login'))

    user = next(
        (u for u in users if u['email'] == user_email),
        None
    )

    if user is None:
        session.pop('user_email', None)
        return redirect(url_for('login'))

    order = {
        'id': str(uuid.uuid4()),
        'user': user['name'],
        'user_email': user_email,
        'items': [dict(item) for item in cart],
        'total': sum(
        item['price'] * item['quantity']
        for item in cart
),
        'status': 'Confirmed',
        'payment_method': 'Simulated Demo Payment',
        'payment_status': 'Simulated successfully — no real money'
    }

    orders.append(order)
    session.pop('cart', None)

    return redirect(url_for('order_history'))


@app.route('/order_history')
def order_history():
    user_email = session.get('user_email')

    if user_email:
        user_orders = [
            order for order in orders
            if order.get("user_email") == user_email
        ]

        return render_template(
            'order_history.html',
            orders=user_orders,
            coffee_journey_demo_enabled=COFFEE_JOURNEY_DEMO_ENABLED,
            csrf_token=get_csrf_token()
        )

    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('index'))

@app.route('/demo/advance-order/<order_id>', methods=['POST'])
def demo_advance_order(order_id):
    if not COFFEE_JOURNEY_DEMO_ENABLED:
        return "Coffee Journey demo controls are disabled.", 403

    submitted_token = request.form.get('csrf_token', '')
    session_token = session.get('_csrf_token', '')

    if not session_token or not secrets.compare_digest(
        submitted_token, session_token
    ):
        return "Invalid or missing CSRF token.", 400

    user_email = session.get('user_email')
    if not user_email:
        return redirect(url_for('login'))

    order = next(
        (
            item for item in orders
            if item.get('id') == order_id
            and item.get('user_email') == user_email
        ),
        None
    )

    if order is None:
        return "Order not found.", 404

    stages = [
        'Confirmed',
        'Brewing',
        'Almost ready',
        'Ready for collection'
    ]

    current_status = order.get('status', 'Confirmed')
    if current_status not in stages:
        return "Invalid order status.", 400

    current_index = stages.index(current_status)
    if current_index < len(stages) - 1:
        order['status'] = stages[current_index + 1]

    return redirect(url_for('order_history'))

if __name__ == '__main__':
    app.run(debug=False)
