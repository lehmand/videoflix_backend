from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def generate_activation_link(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = f"http://vid.daniel-lehmann.dev/activate/{uid}/{token}/"
    return activation_link

def send_confirm_mail(email, username, activation_link):
  subject = "Confirm your email"
  from_email = settings.DEFAULT_FROM_EMAIL

  html_content = render_to_string('emails/confirm_email.html', {
      'username': username.split('@')[0],
      'activation_link': activation_link,
    })
  
  text_content = f"Hallo {username.split('@')[0]}, bitte bestätige deine E-Mail über diesen Link: {activation_link}"
  
  email_msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
  email_msg.attach_alternative(html_content, "text/html")
  email_msg.send()

def send_reset_mail(email, username, reset_link):
    subject = "Reset your password"
    from_email = settings.DEFAULT_FROM_EMAIL

    html_content = render_to_string('emails/forgot_password.html', {
        'username': username.split('@')[0],
        'reset_link': reset_link,
    })
    text_content = f"Hallo {username.split('@')[0]}, bitte führe ein Password reset durch: {reset_link}"
  
    email_msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
    email_msg.attach_alternative(html_content, "text/html")
    email_msg.send()