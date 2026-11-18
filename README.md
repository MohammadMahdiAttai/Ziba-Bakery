# 🥐 Ziba Bakery

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://www.djangoproject.com/)
[![Database](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](#license)

An online storefront and order management system for **Ziba Bakery**, an artisanal bakery and cake shop based in Melbourne, Australia. Built with Django as a university project.

Customers can browse cakes, cupcakes, pastries, and cookies by category, build a cart without needing an account, and complete a simulated two-step checkout with delivery details and card validation. Staff can manage inventory, categories, and customer orders via the customized Django administration panel.

---

## ✨ Features

### 🛒 Customer Storefront
- **Categorized Catalog**: Browse baked goods by categories (*Birthday Cakes*, *Cupcakes*, *Pastries*, *Cookies & Biscuits*).
- **Product Details & Stock**: Detailed product pages with prices in AUD, availability flags, and real-time stock counters.
- **Session-Based Cart**: Add, update, and remove items with dynamic subtotal and total calculations without requiring an upfront account.
- **Two-Step Checkout**:
  1. Delivery address form (auto-filled for authenticated users with saved profile details).
  2. Simulated credit card payment form with client/server validation using the **Luhn algorithm**.
- **Stock Integrity**: Real-time stock verification and atomic transactions (`transaction.atomic`) to deduct inventory safely when an order is placed.
- **User Accounts & Profiles**: User registration, login/logout, profile management (delivery address, suburb, postcode), and order history tracking.
- **Contact & Enquiries**: Contact form connected to Django's email backend.

### 🛠️ Staff & Administration
- Customized Django Admin dashboard (`/admin/`) with Ziba Bakery branding.
- Full CRUD operations for products, categories, orders, order items, and customer profiles.
- Inventory tracking with low-stock visibility.

### 🎨 Frontend & Design
- **"Kraft Bakery Box" Design**: Bespoke warm bakery palette using modern CSS custom properties (no heavy frontend frameworks or build steps required).
- **Responsive Layout**: Mobile navigation drawer with hamburger toggle.
- **User Feedback**: Auto-dismissing alerts and status messages.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.12+, Django 6.0
- **Database**: SQLite
- **Media & Images**: Pillow (for Django `ImageField`)
- **Frontend**: Django Templates, Vanilla HTML5, CSS3, JavaScript (no Node.js build step needed)

---

## 📁 Project Structure

```text
ziba_bakery/
├── ziba_bakery/               # Project configuration (settings, root URLs, WSGI/ASGI)
├── accounts/                  # User registration, login, logout, profile & order history
├── cart/                      # Session-based shopping cart & context processor
├── catalog/                   # Categories & products catalog, fixtures
│   └── fixtures/
│       └── initial_data.json  # Sample bakery menu (4 categories, 12 products)
├── core/                      # Marketing & static pages (Home, About, Contact)
├── orders/                    # Order placement, Luhn payment validation, stock deduction
├── static/
│   ├── css/style.css          # Kraft Bakery Box theme styling
│   └── js/main.js             # Mobile nav toggle & auto-dismiss messages
├── templates/                 # Organized Django HTML templates
│   ├── accounts/
│   ├── cart/
│   ├── catalog/
│   ├── core/
│   ├── orders/
│   └── base.html              # Base master template
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.12 or higher installed on your machine.
- Git.

### 2. Clone the Repository
```bash
git clone https://github.com/MohammadMahdiAttai/Ziba-Bakery.git
cd Ziba-Bakery
```

### 3. Create and Activate a Virtual Environment

- **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (Command Prompt):**
  ```cmd
  python -m venv venv
  venv\Scripts\activate.bat
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run Database Migrations
```bash
python manage.py migrate
```

### 6. Load Sample Bakery Data
Load the initial menu containing 4 categories and 12 sample bakery items:
```bash
python manage.py loaddata initial_data
```

### 7. Create a Superuser (Staff Account)
```bash
python manage.py createsuperuser
```

### 8. Start the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
- **Storefront**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Staff Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 💳 Demo Checkout Instructions

Checkout includes a simulated payment gateway. No real charges or payment processors are involved.

| Field | Demo Value | Note |
| :--- | :--- | :--- |
| **Card Number** | `4242 4242 4242 4242` | Validated via Luhn checksum algorithm |
| **Expiry Date** | Any future date, e.g. `12/28` | Must be formatted as `MM/YY` |
| **CVC** | Any 3 or 4 digits, e.g. `123` | Numeric security code |

> [!NOTE]
> The card number is validated with a real Luhn checksum algorithm. Any invalid number or past expiry date will be rejected by the validation logic. Card details are never saved or stored.

---

## 🗺️ URL Endpoints Overview

| App | Path | Description |
| :--- | :--- | :--- |
| **Core** | `/` | Bakery homepage with featured items |
| | `/about/` | About Ziba Bakery |
| | `/contact/` | Contact & enquiry form |
| **Catalog** | `/shop/` | Full product catalog |
| | `/shop/category/<slug>/` | Filter products by category |
| | `/shop/<id>/<slug>/` | Product detail page |
| **Cart** | `/cart/` | Shopping cart overview |
| | `/cart/add/<product_id>/` | Add or update items in cart (POST) |
| | `/cart/remove/<product_id>/` | Remove item from cart (POST) |
| **Orders** | `/orders/create/` | Step 1: Delivery details form |
| | `/orders/payment/` | Step 2: Simulated card payment form |
| | `/orders/<order_id>/` | Order receipt & confirmation |
| **Accounts** | `/accounts/register/` | Customer sign-up |
| | `/accounts/login/` | Customer login |
| | `/accounts/logout/` | Customer logout |
| | `/accounts/profile/` | Customer profile & order history |
| **Admin** | `/admin/` | Django staff administration portal |

---

## 🔒 Production & Deployment Notes

- `DEBUG = True` and hard-coded `SECRET_KEY` in `ziba_bakery/settings.py` are set for local development convenience.
- When deploying to production:
  - Set `DEBUG = False`.
  - Supply `SECRET_KEY` via an environment variable.
  - Configure `ALLOWED_HOSTS` with your production domain(s).
  - Configure production static/media file serving (e.g., WhiteNoise, AWS S3, or Nginx).

---

## 📄 License

This project was developed for educational and academic portfolio purposes.
