from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def send_verification_email(user_id, domain, protocol):
    """
    Task to send verification email asynchronously
    """
    try:
        user = User.objects.get(id=user_id)
        verification = user.emailverification
        
        context = {
            'user': user,
            'domain': domain,
            'protocol': protocol,
            'token': verification.token,
            'site_name': domain.split('.')[0].title(),
        }
        
        html_content = render_to_string('users/email/verification_email.html', context)
        text_content = strip_tags(html_content)
        
        send_mail(
            subject='Verify your email address',
            message=text_content,
            html_message=html_content,
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        return True
    except Exception as e:
        print(f"Failed to send verification email: {str(e)}")
        return False

@shared_task
def cleanup_expired_verifications():
    """
    Task to cleanup expired verification tokens
    """
    from .models import EmailVerification
    from django.utils import timezone
    
    EmailVerification.objects.filter(
        expires_at__lt=timezone.now(),
        verified_at__isnull=True
    ).delete() 