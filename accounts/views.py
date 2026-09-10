from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from accounts.models import User
from members.models import Member
import re

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact_page(request):
    if request.method == 'POST':
        name    = request.POST.get('contact-name', '')
        email   = request.POST.get('contact-email', '')
        subject = request.POST.get('contact-subject', '')
        message = request.POST.get('contact-message', '')
        if name and email and message:
            from accounts.models import ContactMessage
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            return render(request, 'contact.html', {
                'success': True
            })
    return render(request, 'contact.html')

def public_courses(request):
    from courses.models import Course
    courses = Course.objects.all()
    return render(request, 'courses.html',
                  {'courses': courses})

def public_store(request):
    from store.models import Product
    products = Product.objects.filter(stock__gt=0)
    return render(request, 'store.html',
                  {'products': products})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        role     = request.POST.get('role', 'member')

        # Validation
        if not username:
            return render(request, 'login.html', {
                'error': True,
                'error_msg': 'Username field not empty!'
            })

        if not password:
            return render(request, 'login.html', {
                'error': True,
                'error_msg': 'Password field not empty!'
            })

        if len(password) < 6:
            return render(request, 'login.html', {
                'error': True,
                'error_msg': 'Password consists of at least 6 characters'
            })

        # Email se bhi login ho sake
        from django.contrib.auth import get_user_model
        UserModel = get_user_model()

        try:
            user_obj       = UserModel.objects.get(email=username)
            actual_username = user_obj.username
        except UserModel.DoesNotExist:
            actual_username = username

        user = authenticate(
            request,
            username=actual_username,
            password=password
        )

        if user is not None:
            if user.role != role:
                return render(request, 'login.html', {
                    'error': True,
                    'error_msg': f'This is {user.role} account, Kindly use Correct tab !'
                })
            login(request, user)
            if user.role == 'admin':
                return redirect('/admin-panel/dashboard/')
            elif user.role == 'trainer':
                return redirect('/trainer/dashboard/')
            elif user.role == 'member':
                return redirect('/admin-panel/my-dashboard/')
        else:
            return render(request, 'login.html', {
                'error': True,
                'error_msg': 'Incorrect Username or Password!'
            })

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/login/')

def register_view(request):
    if request.method == 'POST':
        name            = request.POST.get('reg-name', '').strip()
        email           = request.POST.get('reg-email', '').strip()
        phone           = request.POST.get('reg-phone', '').strip()
        age             = request.POST.get('reg-age', '').strip()
        weight          = request.POST.get('reg-weight', '').strip()
        plan            = request.POST.get('reg-membership', '').strip()
        password        = request.POST.get('reg-password', '').strip()
        security_answer = request.POST.get('security_answer', '').strip()

        # Validation
        if not name:
            return render(request, 'register.html', {
                'error': 'Full Name did not empty!'
            })

        if not email:
            return render(request, 'register.html', {
                'error': 'Email did not empty!'
            })
        
        if '@' not in email or '.' not in email:
            return render(request, 'register.html', {
                'error': 'Enter valid email address!(example@gmail.com)'
            })

        if not phone:
            return render(request, 'register.html', {
                'error': 'Phone number did not empty!'
            })

        if len(phone) < 10:
            return render(request, 'register.html', {
                'error': 'Enter valid phone number (At least 10 digits)!'
            })

        if not age:
            return render(request, 'register.html', {
                'error': 'Age did not empty'
            })

        if int(age) < 10 or int(age) > 100:
            return render(request, 'register.html', {
                'error': 'Age is between 15 to 70'
            })

        if not weight:
            return render(request, 'register.html', {
                'error': 'Weight did not empty'
            })

        if not plan:
            return render(request, 'register.html', {
                'error': 'Select Membership plan!'
            })

        if not password:
            return render(request, 'register.html', {
                'error': 'Password did not empty!'
            })

        if len(password) < 6:
            return render(request, 'register.html', {
                'error': 'Password consists of at least 6 charactors!'
            })

        if not security_answer:
            return render(request, 'register.html', {
                'error': 'Security answer did not empty!'
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {
                'error': 'Email already registered!'
            })

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name,
            phone=phone,
            role='member',
            security_answer=security_answer.lower()
        )
        Member.objects.create(
            user=user,
            age=age,
            weight=weight,
            membership_plan=plan
        )
        return redirect('login')

    return render(request, 'register.html')
def forgot_password(request):
    error   = None
    success = None

    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
            # Email sahi hai — session mein save karo
            request.session['reset_email'] = email
            return redirect('/security-question/')
        except User.DoesNotExist:
            error = 'This Email is not registered!'

    return render(request, 'forgot_password.html', {
        'error': error
    })


def security_question(request):
    email = request.session.get('reset_email')

    if not email:
        return redirect('/forgot-password/')

    error = None

    if request.method == 'POST':
        answer = request.POST.get('answer', '').strip().lower()

        try:
            user = User.objects.get(email=email)
            if user.security_answer.lower() == answer:
                request.session['reset_verified'] = True
                return redirect('/reset-password/')
            else:
                error = 'Wrong Answer!'
        except User.DoesNotExist:
            return redirect('/forgot-password/')

    return render(request, 'security_question.html', {
        'error': error
    })


def reset_password(request):
    if not request.session.get('reset_verified'):
        return redirect('/forgot-password/')

    email   = request.session.get('reset_email')
    error   = None
    success = None

    if request.method == 'POST':
        new_password     = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            error = 'Passwords did not match!'
        elif len(new_password) < 6:
            error = 'Password consists of at least 6 Characters!'
        else:
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                # Session clear karo
                del request.session['reset_email']
                del request.session['reset_verified']
                success = 'Password change successfully!'
                return render(request, 'reset_password.html', {
                    'success': success
                })
            except User.DoesNotExist:
                error = 'Error occured, Try Again!.'

    return render(request, 'reset_password.html', {
        'error': error
    })