from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import environ


env = environ.Env()
client = Client(env('TWILIO_ACCOUNT_SID'),env('TWILIO_AUTH_TOKEN'))
verify = client.verify.services(env('TWILIO_VERIFY_SERVICE_SID'))

def send(phone):
    verify.verifications.create(to=phone,channel='sms')

def check(phone,code):
    try:
        result = verify.verification_checks.create(to=phone,code=code)
    except TwilioRestException:
        return False
    return result.status == 'approved'
