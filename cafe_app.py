from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

cafes = [
    {"id": 1, "name": "Green Dot Cafe", "menu": [{"id": 1, "item": "Coffee", "price": 5.0}, {"id": 2, "item": "Tea", "price": 3.0}]},
    {"id": 2, "name": "Goddess Cafe Linden", "menu": [{"id": 1, "item": "Latte", "price": 6.0}, {"id": 2, "item": "Espresso", "price": 4.0}]},
    {"id": 3, "name": "Freshly Ground Coffee", "menu": [{"id": 1, "item": "Mocha", "price": 8.0}, {"id": 2, "item": "Cappuccino", "price": 5.0}]},
]

users = []
orders = []
cart = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        user = {"name": name, "email": email, "phone": phone}
        users.append(user)
        session['user_email'] = email  # store user email in session
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        for user in users:
            if user["email"] == email:
                session['user_email'] = email
                return redirect(url_for('index'))
        return "User not found!"
    return render_template('login.html')

@app.route('/browse_cafes')
def browse_cafes():
    return render_template('browse_cafes.html', cafes=cafes)

@app.route('/add_to_cart/<int:cafe_id>/<int:item_id>')
def add_to_cart(cafe_id, item_id):
    cafe = next((c for c in cafes if c['id'] == cafe_id), None)
    if cafe:
        item = next((i for i in cafe['menu'] if i['id'] == item_id), None)
        if item:
            cart.append(item)
            return redirect(url_for('view_cart'))
    return "Item not found."

@app.route('/view_cart')
def view_cart():
    total = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

@app.route('/place_order', methods=['POST'])
def place_order():
    if not cart:
        return "Your cart is empty!"
    user_email = session.get('user_email')
    if user_email:
        user = next((u for u in users if u["email"] == user_email), None)
        if user:
            order = {
                "user": user["name"],
                "items": cart,
                "total": sum(item["price"] for item in cart)
            }
            orders.append(order)
            cart.clear()
            return redirect(url_for('order_history'))
    return redirect(url_for('login'))

@app.route('/order_history')
def order_history():
    user_email = session.get('user_email')
    if user_email:
        user_orders = [order for order in orders if order["user"] == user_email]
        return render_template('order_history.html', orders=user_orders)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug = True)
