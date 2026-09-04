from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from accounts.models import User
from members.models import Member
from trainers.models import Trainer
from attendance.models import Attendance
from payments.models import Payment
from courses.models import Course
from store.models import Product, Order, OrderItem

# ============================================
# ADMIN CHECK
# ============================================
def admin_check(request):
    if not request.user.is_authenticated:
        return False
    return request.user.role == 'admin'

def member_check(request):
    if not request.user.is_authenticated:
        return False
    return request.user.role == 'member'

# ============================================
# ADMIN VIEWS
# ============================================

def admin_dashboard(request):
    if not admin_check(request):
        return redirect('login')
    today = timezone.now().date()
    
    from django.db.models import Sum
    total_revenue = Payment.objects.filter(
        status='paid'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'total_members':  Member.objects.count(),
        'total_trainers': Trainer.objects.count(),
        'present_today':  Attendance.objects.filter(
            date=today,
            status='present'
        ).count(),
        'total_revenue':  total_revenue,
        'recent_members': Member.objects.select_related(
            'user'
        ).order_by('-join_date')[:5],
        'recent_payments': Payment.objects.select_related(
            'member__user'
        ).order_by('-payment_date')[:5],
    }
    return render(request, 'admin/dashboard.html', context)


def manage_members(request):
    if not admin_check(request):
        return redirect('login')

    errors = []

    if request.method == 'POST':
        name       = request.POST.get('m-name', '').strip()
        email      = request.POST.get('email', '').strip()
        phone      = request.POST.get('phone', '').strip()
        age        = request.POST.get('age', '').strip()
        weight     = request.POST.get('weight', '').strip()
        plan       = request.POST.get('plan', 'basic')
        trainer_id = request.POST.get('trainer_id', '')

        # Validation
        if not name:
            errors.append('Name did not empty!')
        if not email:
            errors.append('Email did not empty!')
        elif '@' not in email:
            errors.append('Enter valid email!')
        elif User.objects.filter(email=email).exists():
            errors.append('Email already registered!')
        if not phone:
            errors.append('Phone did not empty!')
        if not age:
            errors.append('Age did not empty!')
        elif int(age) < 10 or int(age) > 100:
            errors.append('Age is between 15 to 70!')
        if not weight:
            errors.append('Weight did not empty!')
        elif float(weight) < 20:
            errors.append('Enter valid weight!')

        if not errors:
            user = User.objects.create_user(
                username=email,
                email=email,
                password='gymify123',
                first_name=name,
                phone=phone,
                role='member'
            )
            member = Member(
                user=user,
                age=int(age),
                weight=float(weight),
                membership_plan=plan
            )
            if trainer_id:
                member.assigned_trainer = get_object_or_404(
                    Trainer, id=trainer_id)
            member.save()
            return redirect('manage_members')

    trainers = Trainer.objects.select_related('user').all()
    members  = Member.objects.select_related(
        'user', 'assigned_trainer__user'
    ).all()

    return render(request, 'admin/members.html', {
        'members':  members,
        'trainers': trainers,
        'errors':   errors,
    })

def delete_member(request, member_id):
    if not admin_check(request):
        return redirect('login')
    member = get_object_or_404(Member, id=member_id)
    member.user.delete()
    return redirect('manage_members')


def manage_trainers(request):
    if not admin_check(request):
        return redirect('login')

    errors = []

    if request.method == 'POST':
        name   = request.POST.get('t-name', '').strip()
        email  = request.POST.get('email', '').strip()
        phone  = request.POST.get('phone', '').strip()
        spec   = request.POST.get('specialization', 'weight')
        salary = request.POST.get('salary', '').strip()

        # Validation
        if not name:
            errors.append('Trainer name did not empty!')
        if not email:
            errors.append('Email did not empty!')
        elif '@' not in email or '.' not in email:
            errors.append('Enter valid email!')
        elif User.objects.filter(email=email).exists():
            errors.append('Email already registered!')
        if not phone:
            errors.append('Phone did not empty!')
        elif len(phone) < 10:
            errors.append('Enter valid phone number!')
        if not salary:
            errors.append('Salary did not empty!')
        elif int(salary) < 1000:
            errors.append('Salary consistes of at least 1000 PKR!')

        if not errors:
            user = User.objects.create_user(
                username=email,
                email=email,
                password='trainer123',
                first_name=name,
                phone=phone,
                role='trainer'
            )
            Trainer.objects.create(
                user=user,
                specialization=spec,
                salary=salary
            )
            return redirect('manage_trainers')

    trainers = Trainer.objects.select_related('user').all()
    return render(request, 'admin/trainers.html', {
        'trainers': trainers,
        'errors':   errors,
    })


def delete_trainer(request, trainer_id):
    if not admin_check(request):
        return redirect('login')
    trainer = get_object_or_404(Trainer, id=trainer_id)
    trainer.user.delete()
    return redirect('manage_trainers')


def admin_attendance(request):
    if not admin_check(request):
        return redirect('login')
    today   = timezone.now().date()
    records = Attendance.objects.filter(
        date=today
    ).select_related('member__user', 'marked_by__user')
    return render(request, 'admin/attendance.html', {
        'records':       records,
        'present_count': records.filter(status='present').count(),
        'absent_count':  records.filter(status='absent').count(),
        'today':         today,
    })

def admin_payments(request):
    if not admin_check(request):
        return redirect('login')

    from store.models import Order

    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        amount    = request.POST.get('amount')
        method    = request.POST.get('method', 'cash')
        member    = get_object_or_404(Member, id=member_id)
        today     = timezone.now().date()

        # Payment record banao
        Payment.objects.create(
            member=member,
            amount=amount,
            payment_date=today,
            due_date=today,
            method=method,
            status='paid'
        )

        # Is member ke pending orders complete karo
        Order.objects.filter(
            member=member,
            status='pending'
        ).update(status='completed')

        return redirect('admin_payments')

    from django.db.models import Sum
    payments      = Payment.objects.select_related(
                        'member__user'
                    ).order_by('-payment_date')
    members       = Member.objects.select_related('user').all()
    total_revenue = Payment.objects.filter(
                        status='paid'
                    ).aggregate(
                        Sum('amount')
                    )['amount__sum'] or 0

    return render(request, 'admin/payments.html', {
        'payments':      payments,
        'members':       members,
        'paid_count':    payments.filter(status='paid').count(),
        'pending_count': payments.filter(status='pending').count(),
        'total_revenue': total_revenue,
    })

def admin_courses(request):
    if not admin_check(request):
        return redirect('login')
    if request.method == 'POST':
        title       = request.POST.get('title')
        description = request.POST.get('description', '')
        trainer_id  = request.POST.get('trainer_id')
        level       = request.POST.get('level', 'beginner')
        duration    = request.POST.get('duration', '')
        image       = request.FILES.get('image')
        trainer     = get_object_or_404(Trainer, id=trainer_id)
        Course.objects.create(
            title=title,
            description=description,
            trainer=trainer,
            level=level,
            duration=duration,
            image=image
        )
        return redirect('admin_courses')

    all_courses = Course.objects.select_related(
        'trainer__user'
    ).all()
    trainers = Trainer.objects.select_related('user').all()
    return render(request, 'admin/courses.html', {
        'courses':  all_courses,
        'trainers': trainers
    })


def delete_course(request, course_id):
    if not admin_check(request):
        return redirect('login')
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect('admin_courses')


def admin_products(request):
    if not admin_check(request):
        return redirect('login')
    from store.models import Product, Order
    if request.method == 'POST':
        name        = request.POST.get('name')
        description = request.POST.get('description', '')
        category    = request.POST.get('category', 'energy')
        price       = request.POST.get('price')
        stock       = request.POST.get('stock', 0)
        image       = request.FILES.get('image')

        Product.objects.create(
            name=name,
            description=description,
            category=category,
            price=price,
            stock=stock,
            image=image
        )
        return redirect('admin_products')

    products = Product.objects.all()
    orders   = Order.objects.select_related(
        'member__user'
    ).prefetch_related(
        'orderitem_set__product'
    ).order_by('-order_date')

    return render(request, 'admin/products.html', {
        'products': products,
        'orders':   orders,
    })


def admin_reports(request):
    if not admin_check(request):
        return redirect('login')
    from django.db.models import Sum
    context = {
        'total_members':  Member.objects.count(),
        'total_trainers': Trainer.objects.count(),
        'total_revenue':  Payment.objects.filter(
            status='paid'
        ).aggregate(Sum('amount'))['amount__sum'] or 0,
        'total_orders':   Order.objects.count(),
    }
    return render(request, 'admin/reports.html', context)


# ============================================
# MEMBER VIEWS
# ============================================

def member_dashboard(request):
    if not member_check(request):
        return redirect('login')
    member    = request.user.member
    today     = timezone.now().date()
    this_month = today.month
    monthly   = Attendance.objects.filter(
        member=member,
        date__month=this_month
    )
    present = monthly.filter(status='present').count()
    total   = monthly.count()
    percent = int((present / total * 100)) if total > 0 else 0
    return render(request, 'member/dashboard.html', {
        'member':            member,
        'attendance_percent': percent,
        'present_count':     present,
        'recent_attendance': monthly.order_by('-date')[:5],
        'latest_payment':    Payment.objects.filter(
            member=member
        ).order_by('-payment_date').first(),
    })


def member_profile(request):
    if not member_check(request):
        return redirect('login')
    member = request.user.member
    if request.method == 'POST':
        member.user.first_name = request.POST.get(
            'name', member.user.first_name)
        member.user.phone = request.POST.get(
            'phone', member.user.phone)
        member.age    = request.POST.get('age', member.age)
        member.weight = request.POST.get(
            'weight', member.weight)
        member.user.save()
        member.save()
        return redirect('member_profile')
    return render(request, 'member/profile.html', {
        'member': member
    })


def member_attendance(request):
    if not member_check(request):
        return redirect('login')
    member  = request.user.member
    records = Attendance.objects.filter(
        member=member
    ).order_by('-date')
    present = records.filter(status='present').count()
    total   = records.count()
    percent = int((present / total * 100)) if total > 0 else 0
    return render(request, 'member/attendance.html', {
        'records':            records,
        'present_count':      present,
        'absent_count':       records.filter(
                                  status='absent').count(),
        'attendance_percent': percent,
    })


def member_payments(request):
    if not member_check(request):
        return redirect('login')
    member   = request.user.member
    payments = Payment.objects.filter(
        member=member
    ).order_by('-payment_date')
    return render(request, 'member/payments.html', {
        'payments': payments,
        'member':   member,
    })


def member_courses(request):
    if not member_check(request):
        return redirect('login')
    member      = request.user.member
    all_courses = Course.objects.select_related(
        'trainer__user'
    ).all()
    return render(request, 'member/courses.html', {
        'courses': all_courses,
        'member':  member,
    })

def member_course_detail(request, course_id):
    if not member_check(request):
        return redirect('login')
    from courses.models import CourseContent
    course   = get_object_or_404(Course, id=course_id)
    contents = CourseContent.objects.filter(
        course=course
    ).order_by('uploaded_at')
    return render(request, 'member/course_detail.html', {
        'course':   course,
        'contents': contents,
    })

def member_store(request):
    if not member_check(request):
        return redirect('login')

    from store.models import Product

    products  = Product.objects.filter(stock__gt=0)
    cart      = request.session.get('cart', {})
    cart_items = []
    cart_total = 0

    for product_id, quantity in cart.items():
        try:
            product  = Product.objects.get(id=int(product_id))
            subtotal = product.price * quantity
            cart_total += subtotal
            cart_items.append({
                'product':  product,
                'quantity': quantity,
                'subtotal': subtotal,
            })
        except Product.DoesNotExist:
            pass

    return render(request, 'member/store.html', {
        'products':   products,
        'cart_count': len(cart),
        'cart_items': cart_items,
        'cart_total': cart_total,
    })


def add_to_cart(request, product_id):
    cart     = request.session.get('cart', {})
    key      = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    request.session['cart'] = cart
    return redirect('member_store')

def remove_from_cart(request, product_id):
    if not member_check(request):
        return redirect('login')

    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
        request.session.modified = True

    return redirect('member_store')

def checkout(request):
    if not member_check(request):
        return redirect('login')

    from store.models import Product, Order, OrderItem
    from django.contrib import messages

    if request.method == 'POST':
        member          = request.user.member
        payment_method  = request.POST.get('payment_method', 'bank_transfer')
        bank_name       = request.POST.get('bank_name', '').strip()
        account_title   = request.POST.get('account_title', '').strip()
        account_number  = request.POST.get('account_number', '').strip()
        transaction_ref = request.POST.get('transaction_ref', '').strip()
        transfer_amount = request.POST.get('transfer_amount', '').strip()
        cart            = request.session.get('cart', {})

        # Validation
        if not cart:
            messages.error(request, 'Cart is empty!')
            return redirect('member_store')

        if not bank_name:
            messages.error(request, 'Select bank name!')
            return redirect('member_store')

        if not account_title:
            messages.error(request, 'Account title did not empty!')
            return redirect('member_store')

        if not account_number:
            messages.error(request, 'Account number did not empty!')
            return redirect('member_store')

        if not transfer_amount:
            messages.error(request, 'Transfer amount did not empty!')
            return redirect('member_store')

        try:
            # Create Order
            order = Order.objects.create(
                member=member,
                payment_method=payment_method,
                total_amount=0,
                status='pending',
                bank_name=bank_name,
                account_title=account_title,
                account_number=account_number,
                transaction_ref=transaction_ref,
                transfer_amount=transfer_amount
            )

            total = 0
            for product_id, quantity in cart.items():
                try:
                    product  = Product.objects.get(
                        id=int(product_id))
                    subtotal = product.price * int(quantity)
                    total   += subtotal
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=int(quantity),
                        price=product.price
                    )
                    if product.stock >= int(quantity):
                        product.stock -= int(quantity)
                        product.save()
                except Product.DoesNotExist:
                    continue

            order.total_amount = total
            order.save()

            # Cart clear karo
            request.session['cart'] = {}
            request.session.modified = True

            messages.success(
                request,
                'Order placed! Admin will verify your bank transfer.'
            )
            return redirect('member_store')

        except Exception as e:
            print("Checkout Error:", e)
            messages.error(request, 'Error, Try again!')
            return redirect('member_store')

    return redirect('member_store')