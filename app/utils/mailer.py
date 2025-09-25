from flask_mail import Message
from .. import mail  # mail is initialized in __init__.py (like mongo, jwt, bcrypt)

def send_email(subject, recipients, body, sender=("MyApp", "no-reply@myapp.com")):
    """
    Send an email using Flask-Mail.
    
    Args:
        subject (str): Subject of the email.
        recipients (list): List of recipient email addresses.
        body (str): Plain text body of the email.
        sender (tuple): (display_name, email_address).
    """
    try:
        msg = Message(
            subject=subject,
            sender=sender,
            recipients=recipients
        )
        msg.body = body
        mail.send(msg)
        return True, None
    except Exception as e:
        return False, str(e)


def send_otp_email(email, otp , subject= "Verify your email - MyApp"):
    """
    Helper for sending OTP email.
    """
    subject 
    body = f"""
    Hello,

    Your OTP for verifying your account is: {otp}

    This OTP is valid for 10 minutes. 
    Please do not share it with anyone.

    Regards,
    MyApp Team
    """
    return send_email(subject, [email], body)
