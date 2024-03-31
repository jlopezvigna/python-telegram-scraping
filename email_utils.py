import smtplib
from email.message import EmailMessage


def send_email(subject, sender, recipients, password, content, date, username):
    message = EmailMessage()
    message['From'] = sender
    message['To'] = ', '.join(recipients)
    message['Subject'] = subject

    # Add the template and replace the markers
    with open('template.html', 'r') as f:
        html_template = f.read()

    html_content = html_template.format(username=username, date=date, content=content)

    # Add the HTML content to the message
    message.set_content(html_content, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, ) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, message.as_string())
