import smtplib


class SendEmail:
    def __init__(self, email, password, smtp_server, receiver_email):
        self.email = email
        self.password = password
        self.server = smtp_server
        self.receiver_email = receiver_email

    def send_email(self):
        with smtplib.SMTP(self.server) as connection_gmail:
            connection_gmail.starttls()
            connection_gmail.login(user=self.email, password=self.password)
            connection_gmail.sendmail(
                from_addr=self.email,
                to_addrs=self.receiver_email,
                msg=f"Subject: Die ISS ist zu sehen!\n\nZumindest, falls der Himmel frei ist...\n\nLiebe Gruesse\nich"
            )
