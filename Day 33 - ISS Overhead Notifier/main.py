import datetime
import time
from api_requests import WebsiteRequests
from email_logic import SendEmail
import config


MY_EMAIL = config.MY_EMAIL
MY_PASSWORD = config.MY_PASSWORD
SMTP_SERVER = config.SMTP_SERVER
RECEIVER_EMAIL = config.MY_OTHER_EMAIL

now = datetime.datetime.now()
current_time = now.hour * 60 + now.minute
email_bot = SendEmail(MY_EMAIL, MY_PASSWORD, SMTP_SERVER, RECEIVER_EMAIL)

in_range = False


def check_status():
    """
    Checks whether ISS is in range (your location +- )
    Must be broken up into functions!
    Also, python function recursion limit!
    """
    global in_range
    website_requests = WebsiteRequests()
    iss_tuple = website_requests.iss_nearby()
    print("ISS in 4 km range?", iss_tuple[0], " -> ISS distance in km", iss_tuple[1])
    if iss_tuple[1] < 1000:
        if iss_tuple[0]:
            print("ISS in 1000 km range.")
            in_range = True
            if iss_tuple[1] < 4:
                print("ISS in viewing range.")
                daytime = website_requests.check_daytime()
                dusk_time = daytime[0]
                dawn_time = daytime[1]
                if current_time >= dusk_time or current_time <= dawn_time:
                    print("It's dark outside.")
                    clear_sky = website_requests.weather_is_okay()
                    print("Is the sky clear?", clear_sky)
                    print("sleep", 10)
                    time.sleep(10)
                    if clear_sky:
                        email_bot.send_email()
                        print("Email sent to:", config.MY_OTHER_EMAIL)
                        print("sleep", 600)
                        time.sleep(600)
                else:
                    print("It's not dark enough.")
                    print("sleep", 10)
                    time.sleep(10)
            else:
                print("sleep", 30)
                time.sleep(30)
        else:
            if in_range:
                in_range = False
                print("sleep", 1200)
                time.sleep(1200)
            else:
                print("sleep", 60)
                time.sleep(60)
    else:
        print("sleep", 300)
        time.sleep(300)
    check_status()


check_status()
