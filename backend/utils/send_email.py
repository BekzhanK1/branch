from django.contrib import messages
from django.contrib.auth import  get_user_model
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from account.serializers import *
from api.tokens import account_activation_token
from backend.utils import generate_password, send_email


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print('Here')

    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        # messages.success(
        #     request, "Thank you for your email confirmation. Now you can login your account.")
        return render(request, 'login.html')
    # else:
    #     messages.error(request, "Activation link is invalid!")

    return render(request, 'login.html')


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("../templates/template_activate_account.html", {
        'user': user.first_name + " " + user.last_name,
        'domain': "localhost:8000",
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(
            request, f'Problem sending email to {to_email}, check if you typed it correctly.')

