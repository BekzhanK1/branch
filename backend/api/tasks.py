from celery import shared_task

from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import get_template

from account.serializers import *
from api.tokens import account_token

from time import sleep

@shared_task()
def activateEmail(user, domain_name, uid, token, protocol, to_email, template):
    
    # print(user)
    # print(to_email)
    
    mail_subject = "Activate your user account."
    
    template = get_template(template)
    
    html_content = template.render({
        'user': user,
        'domain': domain_name,
        'uid': uid,
        'token': token,
        "protocol": protocol
    })
    # message = render_to_string("../templates/template_activate_account.html", {
    #     'user': user,
    #     'domain': domain_name,
    #     'uid': uid,
    #     'token': token,
    #     "protocol": protocol
    # })
    
    email = EmailMessage(mail_subject, html_content, to=[to_email])
    email.content_subtype = "html"
    email.send()
    
    # if email.send():
    #     messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
    #             received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    # else:
    #     messages.error(
    #         request, f'Problem sending email to {to_email}, check if you typed it correctly.')

@shared_task()
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
    
    print("Email sent")
    
@shared_task()
def send_reset_password_email_to_admin(admin, domain, uid, token, protocol, to_email):
    mail_subject = f"Reset password for {admin}"
    message = render_to_string("../templates/template_reset_admin_password.html", {
        'admin': admin,
        'domain': domain,
        'uid': uid,
        'token': token,
        "protocol": protocol
    })
    
    email = EmailMessage(mail_subject, message, to=[to_email])
    
    email.send()