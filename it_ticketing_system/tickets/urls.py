from django.urls import path
from . import views

urlpatterns = [
    path('', views.TicketListView.as_view(), name='ticket_list'),
    path('create/', views.create_ticket, name='create_ticket'),
    path('ticket/<int:pk>/', views.TicketDetailView.as_view(), name='ticket_detail'),
    path('ticket/<int:pk>/update/', views.update_ticket, name='update_ticket'),
    path('ticket/<int:pk>/assign-to-me/', views.assign_to_me, name='assign_to_me'),
    path('ticket/<int:pk>/delete/', views.delete_ticket, name='delete_ticket'),
    path('admin/delete-closed-tickets/', views.bulk_delete_closed_tickets, name='bulk_delete_closed'),
]
