import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from decouple import config

class AuthNotificationFactory:
    
    @staticmethod
    def register_email_notification(domain_name, user, token, abs_path):
        subject = f"ACCOUNT VERIFICATION"
        absurl = 'http://'+domain_name+abs_path+'?token='+str(token)
        messages = f"Hi {user.first_name}, \n Kindly use below link to activate your email \n  {absurl}"
        print("message: ",messages)
        message = Mail(
            from_email='no-reply@adzplug.com',
            to_emails= user.email,
            subject=subject,
            html_content=messages
        )
        try:
            sg = SendGridAPIClient(config('API_KEY_ID'))
            #os.environ.get('SENDGRID_API_KEY')
            response = sg.send(message)
            return response
        except Exception as e:
            print(e.message)
    
    @staticmethod 
    def send_password_reset_email(domain_name,abs_path,user):
        subject = f"PASSWORD RESET REQUEST"
        absurl = 'http://'+domain_name+abs_path
        messages = f"Hi {user.first_name}, \n Kindly use below link to reset your password \n {absurl}"
        # print("message: ",message)
        message = Mail(
            from_email='no-reply@adzplug.com',
            to_emails= user.email,
            subject=subject,
            html_content=messages
        )
        try:
            sg = SendGridAPIClient(config('API_KEY_ID'))
            response = sg.send(message)
            return response
        except Exception as e:
            print(e.message)