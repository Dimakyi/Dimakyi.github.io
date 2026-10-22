# CaféQuick — Coffee Queue-Free Ordering System

CaféQuick is a Flask-based web application concept that lets customers browse independent, South African-themed cafés, view menus, build a shopping cart, and simulate placing an order.

The project explores the customer journey of a café ordering system, from account registration and menu browsing through checkout and order tracking.

## Features

- **Café discovery:** Browse a collection of themed cafés.
- **Menu browsing:** View menu items for individual cafés.
- **User accounts:** Register with an email address and log in using email or name, with hashed passwords.
- **Shopping cart:** Add items, update quantities, and manage cart contents.
- **Checkout:** Review an order and complete a simulated payment.
- **Order history:** View orders associated with the logged-in account.
- **Demo order tracking:** Progress orders through Confirmed, Brewing, Almost ready, and Ready for collection when demo progression is enabled.
- **CSRF protection:** Validate CSRF tokens on POST requests.
- **Café assistant interface:** A reusable chat-style interface with its own CSS and JavaScript.
- **Automated tests:** Tests covering cart, checkout, login, menus, orders, registration, and demo order progression.

## Technology Stack

- Python
- Flask
- Werkzeug password-hashing utilities
- HTML and CSS
- JavaScript
- Python `unittest`

## Getting Started

### Prerequisites

- Python installed
- Git
- PowerShell on Windows, or an equivalent terminal

### 1. Clone the repository

```bash
git clone https://github.com/Dimakyi/Dimakyi.github.io.git
cd Dimakyi.github.io
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the environment's Python executable directly in the following steps.

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure the Flask secret key

For local development, the application has a fallback secret key. For better session security, set your own secret key in the current PowerShell session before running the app:

```powershell
$env:FLASK_SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
```

Do not commit real secret keys to GitHub.

### 5. Run the application

```powershell
python cafe_app.py
```

Open the local address shown in the terminal, normally `http://127.0.0.1:5000`.

Use the application locally for development and testing. Do not expose Flask's debug server to the public internet.

## Running the Tests

Run the automated test suite from the project directory:

```powershell
python -m unittest discover -v
```

The project has previously passed **28 automated tests** covering key application workflows. Run the suite again after making changes to confirm the current result.

## Current Limitations

CaféQuick is a development/demo application, not a production-ready ordering platform.

- **Simulated payments:** No real payment provider is integrated, and no real payment is processed.
- **In-memory data:** User accounts and orders are stored in Python lists and are lost when the application restarts.
- **Session-based cart:** Cart contents are stored in the user's session.
- **Demo order progression:** Order status changes are simulated, not connected to a real café kitchen or fulfilment system.
- **Pickup scheduling:** A production pickup-time reservation workflow has not been implemented.
- **Production deployment:** Persistent database storage, production secret management, and production server configuration would be needed before real-world use.

## Future Improvements

- Add persistent database storage.
- Integrate a real payment provider in a secure test environment.
- Implement pickup-time selection and order preparation workflows.
- Improve deployment configuration and production security.
- Expand automated testing and user experience improvements.

## Project Purpose

CaféQuick is a practical project for developing and demonstrating skills in Python, Flask, web application development, session handling, password hashing, request validation, and automated testing.

## Repository

[View CaféQuick on GitHub](https://github.com/Dimakyi/Dimakyi.github.io)

