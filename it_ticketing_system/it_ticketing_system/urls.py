from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tickets import views


urlpatterns = [
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
     path('admin/delete-closed-tickets/', views.bulk_delete_closed_tickets, name='bulk_delete_closed'),
    path('admin/', admin.site.urls),
    path('', include('tickets.urls')),  # Include tickets app URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
]
