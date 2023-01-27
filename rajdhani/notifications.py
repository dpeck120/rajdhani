"""Email notifications on bookings.
"""
from . import config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_booking_confirmation_email(booking):
    """Sends a confirmation email on successful booking.

    The argument `booking` is a row in the database that contains the following fields:

        id, name, email, train_number, train_name, ticket_class, date
    """
    # The smtp configuration is available in the config module

    sender_email = "noreply@rajdhani.pipal.in"
    receiver_email = booking['passenger_email']
    message = MIMEMultipart("alternative")
    message["Subject"] = "Booking Confirmation"
    message["From"] = sender_email
    message["To"] = receiver_email

    # write the text/plain part
    text = f"""
            Hi {booking['passenger_name']},

            Your booking has been confirmed.

            Travel date : {booking['departure_date']}
            Train Number : {booking['train_number']}
            Tain Class : {booking['ticket_class']}

            Regards
            Rajdhani
    """

    message.attach(MIMEText(text, "plain"))

    # send your email
    with smtplib.SMTP(config.smtp_hostname, config.smtp_port) as server:
        if config.smtp_username or config.smtp_password:
            server.login(config.smtp_username, config.smtp_password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
