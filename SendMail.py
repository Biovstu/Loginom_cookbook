import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

msg = MIMEMultipart()
sender = 'konstantin.kutovoy@biovitrum.ru'
receiper = 'elena.saveleva@biovitrum.ru'
msg['From'] = sender
msg['To'] = receiper
msg['Subject'] = 'Тест скрипта SMTP'
message = f'Тестовая отправка письма получателю {receiper} и в копии себя {sender}'
msg.attach(MIMEText(message))
try:
    mailserver = smtplib.SMTP_SSL('smtp.yandex.ru',465)
    mailserver.set_debuglevel(True)
    mailserver.login(sender, 'otghxpibwkosvrov')
    mailserver.sendmail(sender,[receiper,sender],msg.as_string())
    mailserver.quit()
    print("Письмо успешно отправлено")
except smtplib.SMTPException:
    print("Ошибка: Невозможно отправить сообщение")