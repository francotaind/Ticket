from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import Ticket, TicketComment, TicketAttachment
from .forms import TicketForm, TicketUpdateForm, CommentForm, AttachmentForm
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


def is_it_staff(user):
    return user.groups.filter(name='IT Staff').exists()

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            
            # Only IT staff can assign tickets to others during creation
            if not (request.user.is_staff or is_it_staff(request.user)):
                ticket.assigned_to = None  # Or assign to default IT person
            
            ticket.save()
            messages.success(request, 'Ticket created successfully!')
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = TicketForm()
    
    return render(request, 'tickets/create_ticket.html', {'form': form})


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'
    
    def get_queryset(self):
        if is_it_staff(self.request.user):
            return Ticket.objects.all().order_by('-created_at')
        else:
            return Ticket.objects.filter(created_by=self.request.user).order_by('-created_at')

class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'tickets/ticket_detail.html'
    context_object_name = 'ticket'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['attachment_form'] = AttachmentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        ticket = self.get_object()
        
        # Check if user has permission to view this ticket
        if not (request.user == ticket.created_by or is_it_staff(request.user)):
            messages.error(request, 'You do not have permission to view this ticket.')
            return redirect('ticket_list')
        
        if 'add_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.ticket = ticket
                comment.author = request.user
                comment.save()
                messages.success(request, 'Comment added successfully!')
        
        elif 'add_attachment' in request.POST:
            attachment_form = AttachmentForm(request.POST, request.FILES)
            if attachment_form.is_valid():
                attachment = attachment_form.save(commit=False)
                attachment.ticket = ticket
                attachment.uploaded_by = request.user
                attachment.save()
                messages.success(request, 'Attachment uploaded successfully!')
        
        return redirect('ticket_detail', pk=ticket.pk)

@login_required
@user_passes_test(is_it_staff)
def update_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    
    if request.method == 'POST':
        form = TicketUpdateForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ticket updated successfully!')
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = TicketUpdateForm(instance=ticket)
    
    return render(request, 'tickets/update_ticket.html', {'form': form, 'ticket': ticket})

@login_required
@user_passes_test(is_it_staff)
def admin_dashboard(request):
    tickets = Ticket.objects.all()
    open_tickets = tickets.filter(status='open')
    in_progress_tickets = tickets.filter(status='in_progress')
    resolved_tickets = tickets.filter(status='resolved')
    closed_tickets = tickets.filter(status='closed')
    
    context = {
        'total_tickets': tickets.count(),
        'open_tickets': open_tickets.count(),
        'in_progress_tickets': in_progress_tickets.count(),
        'resolved_tickets': resolved_tickets.count(),
        'closed_tickets': closed_tickets.count(),
        'recent_tickets': tickets.order_by('-created_at')[:10],
    }
    
    return render(request, 'tickets/admin_dashboard.html', context)

@login_required
@user_passes_test(is_it_staff)
def assign_to_me(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    ticket.assigned_to = request.user
    ticket.status = 'in_progress'
    ticket.save()
    messages.success(request, f'Ticket assigned to you and status changed to In Progress!')
    return redirect('ticket_detail', pk=ticket.pk)


@login_required
@user_passes_test(is_it_staff)
def delete_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    
    if not ticket.is_closed:
        messages.error(request, 'Only closed tickets can be deleted.')
        return redirect('ticket_detail', pk=ticket.pk)
    
    if request.method == 'POST':
        ticket.is_deleted = True
        ticket.deleted_at = timezone.now()
        ticket.deleted_by = request.user
        ticket.save()
        messages.success(request, f'Ticket "{ticket.title}" has been archived.')
        return redirect('ticket_list')

# Optional: Bulk delete closed tickets
@login_required
@user_passes_test(is_it_staff)
def bulk_delete_closed_tickets(request):
    if request.method == 'POST':
        closed_tickets = Ticket.objects.filter(status='closed')
        count = closed_tickets.count()
        
        if count > 0:
            closed_tickets.delete()
            messages.success(request, f'Successfully deleted {count} closed tickets.')
        else:
            messages.info(request, 'No closed tickets to delete.')
        
        return redirect('admin_dashboard')
    
    return redirect('admin_dashboard')



