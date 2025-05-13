from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def generate_activation_link(user):
    """
    Generate a secure one-time activation link for a user.
    
    Creates a unique, time-sensitive link for account activation using Django's
    token generator, which combines the user's ID with a timestamp and 
    cryptographic signing.
    """
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    token = default_token_generator.make_token(user)
    
    activation_link = f"http://vid.daniel-lehmann.dev/api/auth/activate/{uid}/{token}/"
    return activation_link

def send_confirm_mail(email, username, activation_link):
    """
    Send an account activation email to a newly registered user.
    
    Creates and sends both HTML and plain text versions of the confirmation
    email containing the activation link. The email is personalized with
    the user's name (extracted from username).
    """
    subject = "Confirm your email"
    from_email = settings.DEFAULT_FROM_EMAIL

    html_content = render_to_string('emails/confirm_email.html', {
        'username': username.split('@')[0],  # Extract name from email
        'activation_link': activation_link,
    })
  
    text_content = f"Hello {username.split('@')[0]}, please confirm your email with this link: {activation_link}"
  
    email_msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
    email_msg.attach_alternative(html_content, "text/html")
    
    email_msg.send()

def send_reset_mail(email, username, reset_link):
    """
    Send a password reset email to a user.
    
    Creates and sends both HTML and plain text versions of the password reset
    email containing the reset link. The email is personalized with
    the user's name (extracted from username).
    """
    subject = "Reset your password"
    from_email = settings.DEFAULT_FROM_EMAIL

    html_content = render_to_string('emails/forgot_password.html', {
        'username': username.split('@')[0],  # Extract name from email
        'reset_link': reset_link,
    })
    
    text_content = f"Hello {username.split('@')[0]}, please reset your password by clicking this link: {reset_link}"
  
    email_msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
    email_msg.attach_alternative(html_content, "text/html")
    
    email_msg.send()