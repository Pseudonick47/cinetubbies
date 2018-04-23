from authentication.serializers import UserSerializer
from django.core.mail import send_mail

def jwt_response_payload_handler(token, user=None, request=None):
  return {
    'token': token,
    'user': UserSerializer(user, context={'request': request}).data
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