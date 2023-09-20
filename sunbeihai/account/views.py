import logging
from urllib.parse import urlsplit
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse_lazy
from django.utils.translation import activate, gettext as _
from django.conf import settings
from .forms import LoginForm, UserRegistrationForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from .tasks import send_email_async

"""
"""

logging.basicConfig(
    filename='account.log', 
    level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

logger = logging.getLogger(__name__)

"""
"""

User = get_user_model() # Load the custom user model

"""
"""

DEFAULT_HOMEPAGE = 'course:article_list'

"""
"""

def user_login(request):
    """To authenticate a user."""

    is_valid = True
    is_active = True
    next_url = ''

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                        request,
                        username=cd['username'],
                        password=cd['password']
                        )
            if user is None:
                is_valid = False
            elif user.is_active:
                login(request, user)
                activate(request.LANGUAGE_CODE)
                next_url = request.POST.get('next', None)
                redirected_url = next_url if next_url != 'None' else reverse_lazy(DEFAULT_HOMEPAGE)
                return HttpResponseRedirect(redirected_url)
            else:
                is_active = False
    else:
        next_url = request.GET.get('next', None)
        form = LoginForm()

    return render(
        request,
        'account/login.html',
        {
            'form': form,
            'is_valid': is_valid,
            'is_active': is_active,
            'next': next_url
        }
        )

"""
"""

def register(request):
    """To allow new users to register."""

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            try:
                # Create a new user object but avoid saving it yet
                new_user = user_form.save(commit=False)
                # Set the chosen password
                new_user.set_password(user_form.cleaned_data['password'])
                # Save the user object
                new_user.save()
            except Exception as e:
                logger.exception("An error occurred: %s", e)
                return HttpResponseServerError(e)
            
            return render(
                request,
                'account/register_done.html',
                {
                    'new_user': new_user
                }
                )
    else:
        user_form = UserRegistrationForm()

    return render(
        request,
        'account/register.html',
        {
            'user_form': user_form
        }
        )

"""
"""

class UserPasswordChangeView(PasswordChangeView):
    """To customize the password change view."""

    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('account:password_change_done')

"""
"""

class AsyncUserPasswordResetView(PasswordResetView):
    """To customize the password reset view."""
    
    form_class = UserPasswordResetForm
    success_url = reverse_lazy('account:password_reset_done')
    
    def form_valid(self, form):
        # Generate a password reset token and uid
        email = form.cleaned_data["email"]
        users = form.get_users(email)
        
        for user in users:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Build the reset password URL
            current_site = get_current_site(self.request)
            reset_url = f"https://{current_site.domain}/reset/{uid}/{token}/"

            # Email subject and message
            subject = _("密码重置")
            html_message = render_to_string(
                "registration/password_reset_email.html",
                {
                    "user": user,
                    "reset_url": reset_url,
                    "uid": uid,
                    "token": token,
                    "protocol": urlsplit(reset_url).scheme,
                    "domain": current_site.domain,
                    "site_name": _("孙北海的官方网站"),
                },
            )

            # Trigger the Celery task to send email asynchronously
            send_email_async.delay(subject, html_message, settings.EMAIL_HOST_USER, [user.email])
        
        return redirect(self.success_url)

class UserPasswordResetView(PasswordResetView):
    """To customize the password reset view."""
    
    form_class = UserPasswordResetForm
    success_url = reverse_lazy('account:password_reset_done')

"""
"""

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    """To customize the password reset confirm view."""
    
    form_class = UserSetPasswordForm
    success_url = reverse_lazy('account:password_reset_complete')

"""
"""

def page_400(request, exception):
    return render(request, '400.html', status=400)

def page_403(request, exception):
    return render(request, '403.html', status=403)

def page_404(request, exception):
    return render(request, '404.html', status=404)

def page_500(request):
    return render(request, '500.html', status=500)