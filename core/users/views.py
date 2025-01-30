from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import CreateView, TemplateView
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from .models import EmailVerification, User
from django.utils import timezone
from django.utils.html import strip_tags
from .forms import LoginForm, RegisterForm
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.core.exceptions import ValidationError
from .tasks import send_verification_email
# Create your views here.

User = get_user_model()

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        
        # Create email verification token
        verification = EmailVerification.objects.create(user=user)
        
        # Send verification email asynchronously
        current_site = get_current_site(self.request)
        protocol = 'https' if self.request.is_secure() else 'http'
        
        send_verification_email.delay(
            user_id=user.id,
            domain=current_site.domain,
            protocol=protocol
        )
        
        return redirect(reverse('users:verification_sent') + f'?email={user.email}')

    def get_success_url(self):
        return reverse('users:verification_sent') + f'?email={self.object.email}'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users:profile')
        return super().dispatch(request, *args, **kwargs)

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('users:login')

class LoginView(auth_views.LoginView):
    template_name = 'users/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        if next_url and url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure()
        ):
            return next_url
        return reverse('users:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next_url = self.request.GET.get('next')
        if next_url:
            context['next'] = next_url
        return context

    def form_valid(self, form):
        user = form.get_user()
        if not user.email_verified:
            messages.error(self.request, 'Please verify your email address before logging in.')
            return redirect(reverse('users:verification_sent') + f'?email={user.email}')
        return super().form_valid(form)

class EmailVerificationSentView(TemplateView):
    template_name = 'users/verification_sent.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.request.GET.get('email', '')
        return context

def verify_email(request, token):
    verification = get_object_or_404(EmailVerification, token=token)
    
    if verification.is_expired:
        messages.error(request, 'The verification link has expired. Please contact support.')
        return redirect('users:login')
        
    if not verification.is_verified:
        verification.verified_at = timezone.now()
        verification.save()
        verification.user.email_verified = True
        verification.user.save()
        messages.success(request, 'Your email has been verified. You can now login.')
    
    return redirect('users:login')
