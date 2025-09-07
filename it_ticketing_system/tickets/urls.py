from django.urls import path
from . import views

urlpatterns = [
    path('', views.TicketListView.as_view(), name='ticket_list'),
    path('create/', views.create_ticket, name='create_ticket'),
    path('ticket/<int:pk>/', views.TicketDetailView.as_view(), name='ticket_detail'),
    path('ticket/<int:pk>/update/', views.update_ticket, name='update_ticket'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('ticket/<int:pk>/assign-to-me/', views.assign_to_me, name='assign_to_me'),

]
