from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import get_template

from account.serializers import *
from api.tokens import account_token

from time import sleep

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("../templates/template_activate_account.html", {
        'user': user.first_name + " " + user.last_name,
        'domain': "localhost:8000",
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(
            request, f'Problem sending email to {to_email}, check if you typed it correctly.')


def send_credentials_to_employee(user_email, first_name, password, template):
    
    # sleep(10) #To simulate delay
    
    template = get_template(template)

    context = {
        'first_name': first_name,
        'password': password,
    }
    html_content = template.render(context)

    email = EmailMessage(
        "brunch.kz registration complete",
        html_content,
        to=[user_email]
    )
    email.content_subtype = "html"
    email.send()

def send_reset_password_email_to_admin(request ,admin, to_email):
    mail_subject = f"Сброс пароля для {admin.first_name}"
    message = render_to_string("../templates/template_reset_admin_password.html", {
        'admin': admin.first_name + " " + admin.last_name,
        'domain': "localhost:8000",
        'uid': urlsafe_base64_encode(force_bytes(admin.pk)),
        'token': account_token.make_token(admin),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{admin}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(
            request, f'Problem sending email to {to_email}, check if you typed it correctly.')

