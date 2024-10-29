import itertools
import datetime
import os
import requests

def generate_dot_emails(username):
    indices = range(len(username))
    for i in range(1, len(indices) + 1):
        for combination in itertools.combinations(indices, i):
            email = list(username)
            for index in combination:
                email.insert(index, '.')
            yield ''.join(email) + '@gmail.com'

# Read environment variables for username and webhook_url
username = os.getenv('GMAIL_USERNAME')
if not username:
    raise ValueError("GMAIL_USERNAME environment variable is not set")

emails = list(generate_dot_emails(username))

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{username}@gmail.com_emails_{timestamp}.txt"

with open(filename, 'w') as f:
    for email in emails:
        f.write(email + '\n')

print(f"Emails saved to {filename}")

def send_to_discord(emails, webhook_url):
    with open(emails, 'r') as f:
        content = f.read()
    
    payload = {
        'content': content
    }

    response = requests.post(webhook_url, json=payload)
    if response.status_code == 204:
        print("Emails sent to Discord successfully!")
    else:
        print(f"Failed to send emails to Discord. Status code: {response.status_code}")

webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
if not webhook_url:
    raise ValueError("DISCORD_WEBHOOK_URL environment variable is not set")

send_to_discord(filename, webhook_url)
