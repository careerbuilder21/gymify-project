from django.urls import path
from . import views

urlpatterns = [

    # ── ADMIN URLS ──────────────────────────────
    path('dashboard/',
         views.admin_dashboard,
         name='admin_dashboard'),

    path('members/',
         views.manage_members,
         name='manage_members'),

    path('members/delete/<int:member_id>/',
         views.delete_member,
         name='delete_member'),

    path('trainers/',
         views.manage_trainers,
         name='manage_trainers'),

    path('trainers/delete/<int:trainer_id>/',
         views.delete_trainer,
         name='delete_trainer'),

    path('attendance/',
         views.admin_attendance,
         name='admin_attendance'),

    path('payments/',
         views.admin_payments,
         name='admin_payments'),

    path('courses/',
         views.admin_courses,
         name='admin_courses'),
         
    path('courses/delete/<int:course_id>/',
         views.delete_course,
         name='delete_course'),

    path('products/',
         views.admin_products,
         name='admin_products'),

    path('reports/',
         views.admin_reports,
         name='admin_reports'),
         
    path('messages/',
     views.admin_messages,
     name='admin_messages'),

    # ── MEMBER URLS ──────────────────────────────
    path('my-dashboard/',
         views.member_dashboard,
         name='member_dashboard'),

    path('my-profile/',
         views.member_profile,
         name='member_profile'),

    path('my-attendance/',
         views.member_attendance,
         name='member_attendance'),

    path('my-payments/',
         views.member_payments,
         name='member_payments'),

    path('my-courses/',
         views.member_courses,
         name='member_courses'),
         
    path('my-courses/',
         views.member_courses,
         name='member_courses'),

    path('my-courses/<int:course_id>/',
         views.member_course_detail,
         name='member_course_detail'),
    
    path('courses/',
         views.admin_courses,
         name='admin_courses'),

    path('my-store/',
         views.member_store,
         name='member_store'),

    path('cart/add/<int:product_id>/',
         views.add_to_cart,
         name='add_to_cart'),
         
    path('checkout/',
         views.checkout,
         name='checkout'),

    path('cart/remove/<int:product_id>/',
    views.remove_from_cart,
    name='remove_from_cart'),
]