# GYMIFY  "Gym Management System"

This is my Final Year Project for BS Information Technology at Govt MAO Graduate College, Lahore. I built this with my partner Samiullah Khalid under the supervision of Prof. Irfan Shabbir.

The idea came from a real problem like most gyms in Pakistan still use paper registers to track members, payments and attendance. We wanted to build something practical that actually solves this.

## What is GYMIFY?

GYMIFY is a web-based gym management system. It has three types of users (Admin, Trainer, and Member) and each one gets their own dashboard with the tools they need.

The admin (gym owner) manages everything: adding members and trainers, recording payments, uploading workout courses and managing the product store. Trainers can mark attendance, create workout plans, and upload course content. Members can check their attendance, view payment history, access workout courses and buy gym products from the store.


## Features

**For Admin:**
- Add, edit, and delete members and trainers
- Record and track payments
- Monitor attendance
- Manage workout courses and products
- View reports and feedback messages
- Pending orders count on payments page

**For Trainer:**
- Mark daily attendance with date picker 
- Create and upload workout plans
- Track member progress

**For Member:**
- View attendance history and percentage
- Check payment status
- Access workout courses from assigned trainer
- Purchase gym products with bank transfer checkout
- Update profile

**Extra Features:**
- Forgot password using favourite place verification
- Password show/hide on login and register pages
- Contact/feedback form
- Live deployment at gymify.shop with SSL

---

## Tech Stack

| Part | Technology |
|------|-----------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Django |
| Database | MySQL |
| Web Server | Nginx + Gunicorn |
| Hosting | VPS Server (AlmaLinux 9) |
| SSL | Let's Encrypt |

---

## Live Website

The project is live and working at:

**https://gymify.shop**



## How to Run Locally

```bash
# Clone the project
git clone https://github.com/careerbuilder21/gymify-project
cd gymify-project

# Setup virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install requirements
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create admin account
python manage.py createsuperuser

# Start server
python manage.py runserver
```

Then open your browser and go to `http://127.0.0.1:8000`

## Project Structure

```
gymify_project/
├── accounts/       — Login, register, forgot password, contact messages
├── members/        — All admin and member views
├── trainers/       — Trainer views and attendance
├── attendance/     — Attendance model
├── payments/       — Payment model
├── courses/        — Workout courses and uploaded content
├── store/          — Products, orders, cart, checkout
├── templates/
│   ├── admin/      — Admin dashboard pages
│   ├── trainer/    — Trainer dashboard pages
│   ├── member/     — Member dashboard pages
│   └── (public)    — Home, about, store, contact, login, register
└── static/
    ├── css/        — Stylesheet
    ├── js/         — JavaScript
    └── images/     — Images
```

## Payment System

We used manual bank transfer verification instead of EasyPaisa or JazzCash API because those require a registered commercial merchant account. The way it works is simple. Member submits their bank transfer details at checkout and the admin verifies and confirms the payment manually. Once confirmed, the order is marked as completed.

## Team

**Ashar Waseem** — Roll No: 084543  
**Samiullah Khalid** — Roll No: 084546  

**Supervisor:** Prof. Irfan Shabbir  
**Institution:** Govt MAO Graduate College, Lahore  
**Department:** Information Technology  
**Degree:** BS Information Technology (2022–2026)


## Future Plans

There are a few things we want to add in the next version:

- Mobile app (Android/iOS)
- EasyPaisa and JazzCash merchant API for real-time payments
- Biometric attendance
- Email OTP for password recovery
- SMS and email notifications for payments and attendance
- Diet plan management module
- Multi-branch gym support
