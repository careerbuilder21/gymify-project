from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),

    # Public pages
    path('', include('accounts.urls')),
    
    # store 
    path('', include('store.urls')),

    # Admin panel pages
    path('admin-panel/', include('members.urls')),

    # Trainer pages
    path('trainer/', include('trainers.urls')),

] + static(settings.MEDIA_URL,
           document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL,
           document_root=settings.STATIC_ROOT)