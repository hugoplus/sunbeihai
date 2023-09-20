#!/usr/bin/env python
"""Forms for the content in account."""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils.translation import gettext_lazy as _

"""
"""

User = get_user_model()

"""
"""

class LoginForm(forms.Form):
    """Login Form"""

    template_name_label = 'widgets/label.html'

    username = forms.CharField(
        label=_('用户名'), 
        help_text= _('请输入您的用户名'),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
        )
    password = forms.CharField(
        label=_('密码'), 
        help_text= _('请输入您的密码'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
        )
    

class UserRegistrationForm(forms.ModelForm):
    """User Registration Form"""

    password = forms.CharField(
        label=_('密码'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True,
        error_messages={'required': _('请输入密码。')}
        )
    password2 = forms.CharField(
        label=_('确认密码'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True,
        error_messages={'required': _('请再次输入密码。')}
        )
    
    template_name_label = 'widgets/label.html'
    error_css_class = 'text-danger'
    required_css_class = 'required'

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': _('用户名'),
            'first_name': _('名'),
            'last_name': _('姓'),
            'email': _('电子邮箱')
            }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}),
            }
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': _("%(model_name)s 的 %(field_labels)s 已被占用，请重新输入。"),
                }
            }

    def clean_password2(self):
        """To compare the second password against the first one."""

        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            # Translators: This message appears in the registration form.
            raise forms.ValidationError(_('密码不匹配，请重新输入。'))
        return cd['password2']


class UserPasswordChangeForm(PasswordChangeForm):
    """To customize the password change form."""

    template_name_label = 'widgets/label.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize the labels of the form fields
        self.fields['old_password'].label = _('当前密码')
        self.fields['new_password1'].label = _('新密码')
        self.fields['new_password2'].label = _('确认新密码')

        """
        # Customize the help text of the form fields
        self.fields['old_password'].help_text = _('请输入当前密码。')
        self.fields['new_password1'].help_text = _('请输入新密码。')
        self.fields['new_password2'].help_text = _('请重新输入新密码。')
        """

        # Customize the widget attributes of the form fields
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})
        
        
class UserPasswordResetForm(PasswordResetForm):
    """To customize the password reset form."""
    
    template_name_label = 'widgets/label.html'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['email'].label = _('电子邮箱')
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'email'})
        
        
class UserSetPasswordForm(SetPasswordForm):
    """To Customize the form to set new passwords."""
    
    template_name_label = 'widgets/label.html'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['new_password1'].label = _('新密码')
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'new-password'})
        
        self.fields['new_password2'].label = _('确认新密码')
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'new-password'})