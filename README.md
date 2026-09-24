 ## GYMIFY "Gym Management System"

GYMIFY is a web-based gym management system built as a Final Year Project for the Bachelor of Science in Information Technology (2022–2026) at Govt MAO Graduate College, Lahore.
The idea behind this project came from a simple observation. Most gyms in Pakistan still run on paper registers and manual records. Attendance is written by hand, payments are tracked in notebooks and members have no way to check their own history. GYMIFY was built to fix that.

## What It Does

GYMIFY gives every gym three separate dashboards. One for the admin (gym owner), one for trainers and one for members. Each role sees only what they need to see.
**Admin** can add and manage members and trainers, record payments, monitor attendance, upload workout courses, manage the products store, view reports and see feedbacks. Everything the gym owner needs is in one place.
**Trainers** can mark daily attendance for their assigned members, create workout plans, upload course content (PDFs or videos) and keep an eye on member progress. They can also go back and mark attendance for a previous date if they missed it.
**Members** can log in and check their own attendance history, payment records, access workout courses their trainer has uploaded and purchase gym products like protein supplements and energy drinks from the store.

## Tech Stack

 **Frontend:** HTML, CSS, JavaScript
 **Backend:** Python with Django framework
 **Database:** MySQL
 **Server (Live):** Nginx + Gunicorn on Namecheap VPS Spark (AlmaLinux 9)
 **Live URL:** [gymify.shop](https://gymify.shop)
 **SSL:** Let's Encrypt (HTTPS enabled)

## Key Features

- Role-based login system (Admin / Trainer / Member tabs on login page)
- Edit records like members, trainers, products and courses directly without deleting 
- Trainer attendance with date picker and mark today or go back to a previous date
- Bank transfer payment system with admin verification
- Pending orders counter on the payments page
- Forgot password using date of birth verification
- Password show/hide toggle on login and register pages
- Contact/Feedback form and messages saved to database and visible to admin
- Product store with cart, checkout and order tracking
- Course content upload by trainers and they can share PDFs and videos
- Report generation for attendance, payments and product sales
- Fully deployed live with SSL certificate at gymify.shop

## Project Structure

```
gymify_project/
│
├── accounts/          # Login, register, forgot password, contact messages
├── members/           # Admin and member views, all dashboard logic
├── trainers/          # Trainer dashboard, attendance, workout, progress
├── attendance/        # Attendance model
├── payments/          # Payment model
├── courses/           # Course and course content models
├── store/             # Product, order and order item models
├── templates/         # All HTML templates
│   ├── admin/         # Admin dashboard pages
│   ├── trainer/       # Trainer dashboard pages
│   ├── member/        # Member dashboard pages
│   └── ...            # Public pages (home, about, contact, store, courses)
├── static/
│   ├── css/style.css
│   └── js/script.js
└── gymify/            # Django settings, URLs, WSGI
```


## How To Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/careerbuilder21/gymify-project.git
cd gymify-project
```

**2. Create and activate virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Setup MySQL database**
```sql
CREATE DATABASE gymify_db;
```

**5. Run migrations**
```bash
python manage.py migrate
```

**6. Create admin account**
```bash
python manage.py createsuperuser
```

**7. Run the server**
```bash
python manage.py runserver
```

Open your browser and go to: `http://127.0.0.1:8000`

## Live Deployment

The system is live at **gymify.shop** running on:
- Namecheap VPS Spark (AlmaLinux 9)
- Nginx as web server
- Gunicorn as WSGI server
- MySQL database
- SSL via Let's Encrypt (HTTPS)

## Default Login Credentials (Local)

 Role     Email               Password       

 Admin    admin@gymify.pk     Gymify@2026!   
 Trainer  (set by admin)      trainer123     
 Member   (set by admin)      gymify123      

Members can also self-register through the registration page.

## Developed By

Ashar Waseem            084543          
Samiullah Khalid        084546          

**Supervised by:** Prof. Irfan Shabbir  
**Institution:** Govt MAO Graduate College, Lahore  
**Department:** Information Technology (FCIT)  
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
