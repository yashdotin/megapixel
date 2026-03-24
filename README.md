Megapixel

<p align="center">
  A modern photography portfolio & client gallery platform built with Django
</p><p align="center">
  <img src="https://img.shields.io/badge/Django-Backend-green?style=flat-square" />
  <img src="https://img.shields.io/badge/PostgreSQL-Database-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/Cloudinary-Media-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/Status-Active-success?style=flat-square" />
</p>---

✦ What is Megapixel?

Megapixel is a photography-focused web platform designed to showcase work, manage client galleries, and handle inquiries — all in one place.

Instead of juggling multiple tools, this gives photographers a single clean system to:

- present their portfolio
- deliver client photos
- manage communication

---

✦ Core Features

Portfolio System

- Create and display photography projects
- Category-based filtering
- Detailed project pages with metadata

Client Galleries

- Private & public galleries
- Client-specific image collections
- Clean viewing experience

Authentication

- Signup / Login / Logout
- Profile management
- Editable user details

Communication

- Contact form with database storage
- Email notification system
- OTP-based email verification

Services Section

- Showcase photography packages
- Simple pricing display

---

✦ Tech Stack

Layer| Technology
Backend| Django
Language| Python
Frontend| HTML, CSS, JavaScript
Database| PostgreSQL
Media| Cloudinary
Deployment| Gunicorn + WhiteNoise

---

✦ Project Structure

megapixel/
├── manage.py
├── requirements.txt
├── accounts/
├── core/
├── templates/
├── static/
├── media/
└── megapixel/
    ├── settings.py
    ├── urls.py
    └── wsgi.py

---

✦ Getting Started

1. Clone the repo

git clone https://github.com/yashdotin/megapixel.git
cd megapixel

2. Setup environment

python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux

3. Install dependencies

pip install -r requirements.txt

4. Configure environment variables

Create ".env" file:

SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
EMAIL_HOST_PASSWORD=your_email_password

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

5. Run project

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

---

✦ Routes Overview

Route| Description
"/"| Home
"/projects/"| Portfolio
"/services/"| Services
"/contact/"| Contact
"/profile/"| User Profile
"/client-galleries/"| Client Work

---

✦ Why This Project Matters


It combines:

- real-world use case (photography business)
- authentication + email workflows
- media handling (Cloudinary)
- structured Django architecture

That makes it portfolio-worthy, not just practice.

---
 these and this project jumps a level.



---

✦ Author

Yash
BTech Student | Aspiring AI/ML Engineer

---

