from email.mime.text import MIMEText
import smtplib

def send_email(email, height, avg_height, cnt_height):
    from_email = 'annvt.dl@gmail.com'
    from_passwd = '********'
    to_email = email
    subject = 'Height Data'
    message = 'Hey there, your height is %s. Average height of all is %s. And that is calculated out of %s people.' % (height, avg_height, cnt_height)

    msg=MIMEText(message, 'html')
    msg['Subject']=subject
    msg['To']=to_email
    msg['From']=from_email

    gmail=smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_passwd)
    gmail.send_message(msg)