from django import forms
from django.utils.translation import ugettext_lazy

from .models import Active, Email


class EmailAddForm(forms.ModelForm):

    class Meta:
        model = Email
        fields = (
            'alert_email',
        )
        labels = {
            'alert_email': ugettext_lazy('New email address for alerting'),
        }


class EmailDeleteForm(forms.ModelForm):

    class Meta:
        model = Email
        fields = (
            'alert_email',
        )


class ActiveAddForm(forms.ModelForm):

    class Meta:
        model = Active
        fields = (
            'active_name', 'active_token', 'active_hostname', 'active_ip', 
            'active_description', 'active_cpu_limit', 'active_ram_limit', 
            'active_swap_limit',
        )
        labels = {
            'active_name': ugettext_lazy('Name (for monitoring)'),
            'active_token': ugettext_lazy('Token for API'),
            'active_ip': ugettext_lazy('Real IP address'),
            'active_hostname': ugettext_lazy('Real hostname'),
            'active_description': ugettext_lazy('Any description'),
            'active_cpu_limit': ugettext_lazy('CPU limit for alerting'),
            'active_ram_limit': ugettext_lazy('RAM limit for alerting'),
            'active_swap_limit': ugettext_lazy('SWAP limit for alerting'),
        }
        widgets = {
            'active_name': forms.Textarea(attrs={'cols': 50, 'rows': 1}),
            'active_token': forms.Textarea(attrs={'cols': 50, 'rows': 1}),
            'active_ip': forms.Textarea(attrs={'cols': 50, 'rows': 1}),
            'active_hostname': forms.Textarea(attrs={'cols': 50, 'rows': 1}),
            'active_description': forms.Textarea(attrs={'cols': 50, 'rows': 10}),
            'active_cpu_limit': forms.NumberInput(attrs={'cols': 5, 'rows': 1}),
            'active_ram_limit': forms.NumberInput(attrs={'cols': 5, 'rows': 1}),
            'active_swap_limit': forms.NumberInput(attrs={'cols': 5, 'rows': 1}),
        }


class ActiveEditForm(forms.ModelForm):

    class Meta:
        model = Active
        fields = (
            'active_name', 'active_token', 'active_hostname', 'active_ip', 
            'active_description', 'active_cpu_limit', 'active_ram_limit', 
            'active_swap_limit',
        )
        labels = {
            'active_name': ugettext_lazy('Name (for monitoring)'),
            'active_token': ugettext_lazy('Token for API'),
            'active_ip': ugettext_lazy('Real IP address'),
            'active_hostname': ugettext_lazy('Real hostname'),
            'active_description': ugettext_lazy('Any description'),
            'active_cpu_limit': ugettext_lazy('CPU limit for alerting'),
            'active_ram_limit': ugettext_lazy('RAM limit for alerting'),
            'active_swap_limit': ugettext_lazy('SWAP limit for alerting'),
        }
        widgets = {
            'active_name': forms.Textarea(attrs={'cols': 50, 'rows': 1}),
            'active_token': forms.Textarea(attrs={'cols': 50, 'rows': 1}),
            'active_ip': forms.Textarea(attrs={'cols': 50, 'rows': 1}),
            'active_hostname': forms.Textarea(attrs={'cols': 50, 'rows': 1}),
            'active_description': forms.Textarea(attrs={'cols': 50, 'rows': 10}),
            'active_cpu_limit': forms.NumberInput(attrs={'cols': 5, 'rows': 1}),
            'active_ram_limit': forms.NumberInput(attrs={'cols': 5, 'rows': 1}),
            'active_swap_limit': forms.NumberInput(attrs={'cols': 5, 'rows': 1}),
        }