# 🛒 POS System – Django + Bootstrap 5

A modern **Point of Sale (POS) System** built with **Django** and **Bootstrap 5**, designed for small businesses.

This project is structured for both development and production environments:
- 🧪 SQLite (Development)
- 🐘 PostgreSQL (Production)
- 🔐 Environment variable configuration
- 📦 Production-ready settings

---

## 🚀 Features

- Product & Category Management
- Sales & Invoice Tracking
- User Authentication & Authorization
- Django Admin Customization
- Static & Media File Handling
- Email Configuration Support
- Environment-based Settings (`.env`)

---

## 🛠 Tech Stack

- Python 3.10+
- Django
- Bootstrap 5
- SQLite (Development)
- PostgreSQL (Production)

---

## 📋 Requirements

- Python 3.10+
- pip
- Git
- Virtualenv (recommended)

---

## 📥 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/code-masud/pos.git
cd pos
```

---

### 2️⃣ Create and Activate Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Setup Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Update `.env` with your configuration:

```env
SECRET_KEY=your-secret-key
DEBUG=True

ALLOWED_HOSTS=127.0.0.1,localhost

# Database
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password

# Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

---

### 5️⃣ Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

---

### 7️⃣ Run Development Server

```bash
python manage.py runserver
```

Visit:

- Main App → http://127.0.0.1:8000/
- Admin Panel → http://127.0.0.1:8000/admin/

---
