from django import forms
from .models import Ticket, TicketComment, TicketAttachment

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status', 'priority', 'assigned_to']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show IT staff users in assigned_to field
        self.fields['assigned_to'].queryset = self.fields['assigned_to'].queryset.filter(
            groups__name='IT Staff'
        )

class CommentForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ['content', 'is_internal']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = TicketAttachment
        fields = ['file']
