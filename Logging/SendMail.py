import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Здесь может быть код работы с данными
LOGIN = ''
PASSWORD = ''
TO = ''
SUBJECT = ''
MESSAGE = ''

msg = MIMEMultipart()
msg['From'] = LOGIN
msg['To'] = TO
msg['Subject'] = SUBJECT
message = MESSAGE
msg.attach(MIMEText(message))
try:
    mailserver = smtplib.SMTP_SSL('smtp.yandex.ru',465)
    mailserver.set_debuglevel(True)
    mailserver.login(LOGIN, PASSWORD)
    mailserver.sendmail(LOGIN,[TO,LOGIN],msg.as_string())
    mailserver.quit()
    res = 'Письмо успешно отправлено'
    print(res)
except smtplib.SMTPException:
    res = 'Ошибка: Невозможно отправить сообщение'
    print(res)