from django import forms

from .models import Active


class ActiveForm(forms.ModelForm):

    class Meta:
        model = Active
        fields = ('active_name', 'active_token', 'active_hostname', 
                  'active_ip', 'active_description', )


class ActiveEditForm(forms.ModelForm):

    class Meta:
        model = Active
        fields = ('active_name', 'active_token', 'active_hostname', 
                  'active_ip', 'active_description', )


class ActiveDeleteForm(forms.ModelForm):

    class Meta:
        model = Active
        fields = ('active_name', 'active_hostname', 'active_ip', 
                  'active_description', )
