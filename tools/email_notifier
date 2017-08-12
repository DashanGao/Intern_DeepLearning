from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

# smtp server
host_server = 'smtp.XX.com'
sender_qq = '7949XXXXX'
pwd = 'kozv*********e'
sender_qq_mail = 'da****gao@foxmail.com'
receiver = 'mountg*****@gmail.com'


def send(mail_content, mail_title='Malong Notification'):
    smtp = SMTP_SSL(host_server)
    smtp.ehlo(host_server)
    smtp.login(sender_qq, pwd)

    msg = MIMEText(mail_content, "plain", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq_mail
    msg["To"] = receiver
    smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
    smtp.quit()
