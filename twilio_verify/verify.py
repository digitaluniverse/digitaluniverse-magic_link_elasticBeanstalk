from twilio.rest import Client
from decouple import config

TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
TWILIO_VERIFICATION_SID=config('TWILIO_VERIFICATION_SID')


client = Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)





def verifications(to, channel_configuration):
	return client.verify \
		.services(TWILIO_VERIFICATION_SID) \
		.verifications \
		.create(
			to=to,
			channel="email",
			channel_configuration=channel_configuration
		)

def verification_checks(to, token):
	return client.verify \
		.services(TWILIO_VERIFICATION_SID) \
		.verification_checks \
		.create(to=to, code=token)
        
def get_channel_configuration(to,callback_url):
    channel_configuration={
        #used in email template
        'substitutions': {
            'email': to,
            'callback_url': callback_url
        }
    }
    return channel_configuration

