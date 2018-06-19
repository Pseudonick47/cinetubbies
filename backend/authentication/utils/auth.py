import random
import string


from django.core.mail import send_mail

from authentication.serializers import AdminSerializer


CHAR_SET = string.digits + string.ascii_letters

def jwt_response_payload_handler(token, user=None, request=None):
  return {
    'token': token,
    'user': AdminSerializer(user, context={'request': request}).data
  }

def send_email(mail_subject, mail_from, mail_to, mail_message):
  try:
    send_mail(
      mail_subject,
      mail_message,
      mail_from,
      [mail_to],
      fail_silently=False,
    )
  except Exception:
    pass

def send_verification_mail(user, token):
  message = f"""
    Hello, welcome to Cinetubbies
    Please go to link to verify the email
    ovo.je/neki/link/{token}
  """
  send_email(
    'Verify Your Account',
    'tinkivinki@cinetubbies.com',
    user.email,
    message
  )

def send_mail_to_admin(user, single_use_token, token):
  message = f"""
    Hello, welcome to Cinetubbies
    You are now able to login to our services. We have generated for you a
    single use token and it will become invalid on you first login. You will
    be prompted to enter a new password, please don't leave the page before you
    confirm your new password.

    To verify your email and login for the first time, visit:
    http://localhost:8080/set-password/{single_use_token}

    Sincerely,
    Cinetubbies Team
  """

  send_email(
    'Account information',
    'tinkivinki@cinetubbies.com',
    user.email,
    message
  )

def send_invitation_mail(user, id):
  message = f"""
    You have been invited to show. If you would like to accept click on the link:
    http://localhost:8080/accept-invite/{id}

  """
  send_email(
    'Invitation',
    'tinkivinki@cinetubbies.com',
    user.email,
    message
  )

def generate_password(num_of_chars=12):
  return ''.join([random.choice(CHAR_SET) for _ in range(12)])

def generate_single_use_token(num_of_chars=32):
  return ''.join([random.choice(CHAR_SET) for _ in range(32)])
