import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr


def send_email(subject, sender, recipients, password, content, date, username, attachment_path=None):
    message = MIMEMultipart()
    message['From'] = formataddr(("SimplyDevTools", sender))
    message['To'] = ', '.join(recipients)
    message['Subject'] = subject

    # Add the template and replace the markers
    with open('template.html', 'r') as f:
        html_template = f.read()

    html_content = html_template.format(username=username, date=date, content=content)

    # Add the HTML content to the message
    message.attach(MIMEText(html_content, 'html'))

    # Add attachment
    if attachment_path:
        with open(attachment_path, 'rb') as attachment_file:
            attachment = MIMEApplication(attachment_file.read(), Name=attachment_path)
            attachment['Content-Disposition'] = f'attachment; filename="{attachment_path}"'
            message.attach(attachment)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, ) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, message.as_string())
