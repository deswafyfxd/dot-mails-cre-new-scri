import itertools
import datetime
import os
import requests  # Make sure this import is at the top

def generate_dot_emails(username):
    indices = range(len(username))
    for i in range(1, len(indices) + 1):
        for combination in itertools.combinations(indices, i):
            email = list(username)
            for index in combination:
                email.insert(index, '.')
            yield ''.join(email) + '@gmail.com'

username = os.getenv('GMAIL_USERNAME')
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
send_to_discord(filename, webhook_url)
