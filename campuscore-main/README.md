# CampusCore — Event Management System

A full-stack event management web application built for SIST college, featuring role-based access for **Admins**, **Organisers**, and **Students**.

## Features

- 🔐 Role-based authentication (Admin / Organiser / Student)
- 📅 End-to-end event lifecycle (Create → Approve → Register → Attend → Certificate)
- 📷 QR-code based attendance tracking
- 📡 Real-time updates via Socket.IO (live attendance counter + announcements)
- 📧 Email notifications (Node.js microservice)
- 📊 Admin analytics dashboard
- 🎓 PDF certificate generation

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python / Flask |
| Database | SQLite (via SQLAlchemy ORM) |
| Realtime | Flask-SocketIO |
| Email | Node.js microservice |
| Frontend | Vanilla HTML/CSS/JS (custom design system) |

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/Kxhor/Campus-core.git
cd Campus-core
```

### 2. Set up a virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the root directory:
```
SECRET_KEY=your_random_secret_key
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
INJECT_DEMO_DATA=true   # Only for local dev
FLASK_DEBUG=True        # Only for local dev
```

### 5. Run the app
```bash
python app_legacy.py
```

Open `http://127.0.0.1:5000` in your browser.

### Demo Credentials (local dev only, requires INJECT_DEMO_DATA=true)
| Role | Email | Password |
|---|---|---|
| Admin | admin@sist.ac.in | admin123 |
| Organiser | organizer@sist.ac.in | organizer123 |
| Student | student@sist.ac.in | student123 |

> ⚠️ **Never deploy with `INJECT_DEMO_DATA=true` or `FLASK_DEBUG=True` in production.**

## Security

This project has been through a comprehensive 13-point security audit:
- Role-based auth decorators on every endpoint
- Rate limiting on login and QR scan endpoints
- Input sanitization on all user-submitted data
- HTTPS enforcement in production
- Secure, HttpOnly, SameSite session cookies
- No hardcoded secrets (all via `.env`)
- Demo data locked behind environment variable

## License

For academic/institutional use — SIST College.
