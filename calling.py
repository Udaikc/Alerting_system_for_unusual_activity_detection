import os
from twilio.rest import Client

# Set up Twilio credentials (make sure to store them securely in environment variables)
account_sid = ""
auth_token = ""

# Create a Twilio client
client = Client(account_sid, auth_token)

# Make a phone call
call = client.calls.create(
    url="",  # URL for the TwiML response
    to="",  # The phone number you want to call
    from_=""  # Your Twilio phone number
)

# Print the SID of the call for tracking purposes
print(f"Call SID: {call.sid}")


#this definitely will call
