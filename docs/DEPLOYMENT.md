# CampusCore Deployment Guide

## 1. What This App Is
CampusCore is a full-stack web application designed for college event management. It allows event organizers to create and manage events, administrators to approve them, and students to seamlessly register and attend. The system handles the entire lifecycle, including live QR-code attendance tracking on the day of the event and automatic generation of PDF certificates once the event is completed.

## 2. Server Requirements
- **Operating System:** Ubuntu 22.04 LTS or Windows Server 2019+
- **Python:** 3.11 or higher
- **Memory:** 1GB RAM minimum, 2GB recommended
- **Storage:** 10GB disk space minimum
- **Network:** Ports 80 and 443 open (or 5000 for internal use)

## 3. Step-by-Step Installation
1. Install Python 3.11 on your server.
2. Download or clone the project folder to your server.
3. Open a terminal in the project folder.
4. Run: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env`
6. Fill in the `.env` file (refer to section 4 below).
7. Run: `flask db upgrade` (sets up the database).
8. Start the app (see section 5).

## 4. Configuration (.env file)
- `SECRET_KEY`: A long random password for the app. Generate with Python.
- `DATABASE_URL`: Leave as `sqlite:///campuscore.db` unless using PostgreSQL.
- `FORCE_HTTPS`: Set to `True` only after SSL is installed.
- `MAIL_SERVER` / `MAIL_USERNAME` / `MAIL_PASSWORD`: Your college SMTP server details.
- `ALLOWED_ORIGINS`: The URL where your college will access the app.
- `INJECT_DEMO_DATA`: Leave as `False` in production.
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`: Only needed if enabling Google login.

## 5. Starting and Stopping the App

**For Linux/Ubuntu:**
- **Start:** `gunicorn -w 4 -b 0.0.0.0:5000 "app_legacy:app" &`
- **Stop:** `pkill gunicorn`

**For Windows:**
- **Start:** `waitress-serve --port=5000 app_legacy:app`
- **Stop:** Close the terminal or press `Ctrl+C`

*Note: The app must be actively running on the server for students to access it. If the server restarts, you need to start the app again. It is highly recommended to set up a systemd service (Linux) or Windows Service for automatic startup.*

## 6. Setting Up a systemd Service (Linux only)
To keep the app running in the background and automatically restart on server reboots, create a file at `/etc/systemd/system/campuscore.service` with the following content:

```ini
[Unit]
Description=Gunicorn instance to serve CampusCore
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/path/to/campuscore
Environment="PATH=/path/to/campuscore/venv/bin"
ExecStart=/path/to/campuscore/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 "app_legacy:app"

[Install]
WantedBy=multi-user.target
```

Enable and start the service with:
```bash
sudo systemctl enable campuscore
sudo systemctl start campuscore
```

## 7. Email Configuration
The app automatically sends emails for:
- Student registration confirmations
- Password resets
- New user notifications

To set this up, fill in the `.env` variables for your institutional SMTP server or a standard Gmail App Password. For example:
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## 8. SSL / HTTPS
HTTPS is required for production to keep user data secure. We recommend using Let's Encrypt (free) via Certbot. Once SSL is working and the app is served over HTTPS, set `FORCE_HTTPS=True` in your `.env` file and restart the app.

## 9. First-Time Setup
An admin account must be created after the first launch to manage the platform.
- **Option A:** Set `INJECT_DEMO_DATA=True` in `.env` on first run (this creates an admin account `admin@sist.ac.in` with the password `admin123`). Log in, immediately change the password, then set `INJECT_DEMO_DATA=False` and restart the app.
- **Option B:** Register manually via the `/register` page and then manually change your role to `admin` directly inside the database.

## 10. Backup
- The database file is: `campuscore.db` (in the project root)
- User uploads are in: `static/uploads/`
Back up both weekly. Copy them to a separate drive or cloud storage to prevent data loss.

## 11. Common Problems
- **App won't start:** Check Python version (must be 3.11+). Check if `.env` exists.
- **Emails not sending:** Check `MAIL_SERVER` and `MAIL_PASSWORD` in `.env`.
- **Site not loading after SSL:** Check `FORCE_HTTPS` is `True` and port 443 is open on your firewall.
- **Database locked error:** This happens under heavy traffic. Upgrade `DATABASE_URL` to PostgreSQL.

## 12. Contact
Kishor G & Hemanth Raj
Built for Sathyabama Institute of Science and Technology
