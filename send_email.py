import smtplib

email = "connitdevs@gmail.com"


def send_email(receiver, subject, message):
    global email
    try:
        text = f"Subject: {subject}\n\n{message}"
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, "zeibftsoamrlpgln")
        server.sendmail(email, receiver, text)
        return True
    except:
        return False



