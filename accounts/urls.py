from django.urls import path
from . import views

urlpatterns = [
    path('',
         views.home,
         name='home'),

    path('about/',
         views.about,
         name='about'),

    path('contact/',
         views.contact_page,
         name='contact'),

    path('login/',
         views.login_view,
         name='login'),

    path('logout/',
         views.logout_view,
         name='logout'),

    path('register/',
         views.register_view,
         name='register'),

    path('courses/',
         views.public_courses,
         name='public_courses'),

    path('store/',
         views.public_store,
         name='public_store'),

    path('forgot-password/',
         views.forgot_password,
         name='forgot_password'),

    path('security-question/',
         views.security_question,
         name='security_question'),

    path('reset-password/',
         views.reset_password,
         name='reset_password'),
]