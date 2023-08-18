import smtplib
from email.message import EmailMessage

def email(subject,body,to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to']= to
    user = "opencvmob@gmail.com"
    msg['from'] =user
    password ="iestnkclnouvsyrp"

    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

if __name__ == '__main__':
    email("HELLO!","THE STATUS OF THE MANHOLE","eceembedded02@gmail.com")