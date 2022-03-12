from twilio.rest import Client
account_sid="AC1cecbc0e8f1cf504dbf7a81b91ee6592"
auth_token="50b3fef58d2789ffaef9a7eadecce170"
client=Client(account_sid,auth_token)
message=client.api.account.messages.create(
to="+959963295100",from_="+15012632070",body="This is alert!")
print("Send message successfully!")
