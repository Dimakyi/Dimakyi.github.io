# CaféQuick — Coffee Queue-Free Ordering System

CaféQuick is a Python and Flask web application concept for exploring a queue-free café ordering experience. Customers can browse themed, South African-inspired cafés, view menus, manage a shopping cart, and complete a simulated checkout.

The project demonstrates practical web development skills across account management, session handling, request security, order workflows, and automated testing.

## Features

- **Café discovery:** Browse a collection of themed cafés.
- **Menu browsing:** View menu items for individual cafés.
- **User registration and login:** Create an account and log in using an email address or name, with password hashing.
- **Shopping cart:** Add items, update quantities, and manage cart contents.
- **Simulated checkout:** Review an order and complete a demo payment flow.
- **Order history:** View orders associated with the logged-in account.
- **Demo order tracking:** Progress orders through Confirmed, Brewing, Almost ready, and Ready for collection when demo progression is enabled.
- **CSRF protection:** Validate CSRF tokens on POST requests.
- **Café assistant interface:** Provide a reusable chat-style interface supported by its own CSS and JavaScript.
- **Automated testing:** Test key application workflows, including registration, login, menus, cart operations, checkout, orders, and demo order progression.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Flask | Web application framework |
| Werkzeug | Password-hashing utilities |
| HTML | Page structure |
| CSS | Styling and layout |
| JavaScript | Client-side interactions |
| Python `unittest` | Automated tests |

## Getting Started

### Prerequisites

- Python
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

If PowerShell blocks environment activation, use the virtual environment's Python executable directly in the following steps.

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure the Flask secret key

For local development, the application has a fallback secret key. For better session security, generate a secret key for your current PowerShell session:

```powershell
$env:FLASK_SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
```

Keep real secret keys out of source control.

### 5. Run the application

```powershell
python cafe_app.py
```

Open the local address shown in the terminal, normally:

`http://127.0.0.1:5000`

Use Flask's development server for local development only. Do not expose it directly to the public internet.

## Running the Tests

**Testing evidence:** The project currently passes all 28 automated tests covering key application workflows. Run the test suite again after making changes to verify the result.

```powershell
python -m unittest discover -v
```

**Testing evidence:** The project previously passed 28 automated tests covering key application workflows. Run the test suite again after changes to verify the current result.

## Current Limitations

CaféQuick is a development and demonstration project, not a production-ready ordering platform.

- **Simulated payments:** No real payment provider is integrated, and no real payments are processed.
- **In-memory data:** User accounts and orders are stored in Python lists and are lost when the application restarts.
- **Session-based cart:** Cart contents are stored in the user's session.
- **Simulated order progression:** Order status changes are not connected to a real café kitchen or fulfilment system.
- **Pickup scheduling:** A production pickup-time reservation workflow has not been implemented.
- **Production deployment:** Persistent database storage, production-grade secret management, and appropriate server configuration would be needed before real-world use.

## Future Improvements

- Introduce persistent database storage for users and orders.
- Integrate a payment provider using a secure test environment.
- Add pickup-time selection and order preparation workflows.
- Improve deployment configuration and production security.
- Expand automated test coverage and improve the customer experience.

## Project Purpose

CaféQuick is a hands-on project for developing and demonstrating skills in Python, Flask, web application development, session management, password hashing, request validation, and automated testing.

## Repository

[View CaféQuick on GitHub](https://github.com/Dimakyi/Dimakyi.github.io)
