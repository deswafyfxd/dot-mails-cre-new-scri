import itertools
import datetime
import os
import requests

def generate_dot_emails(username, max_emails=None):
    indices = range(1, len(username))  # Start from index 1 to avoid leading dots
    count = 0
    for i in range(1, len(indices) + 1):
        for combination in itertools.combinations(indices, i):
            if max_emails and count >= max_emails:
                return
            email = list(username)
            for index in combination:
                email.insert(index, '.')
            dotted_email = ''.join(email) + '@gmail.com'
            if '..' not in dotted_email:  # Ensure no double dots
                yield dotted_email
                count += 1

# Read environment variables for username and webhook_url
username = os.getenv('GMAIL_USERNAME')
if not username:
    raise ValueError("GMAIL_USERNAME environment variable is not set")

default_creation = os.getenv('DEFAULT_CREATION', 'false').lower() == 'true'
max_emails = os.getenv('MAX_EMAILS')

if default_creation:
    max_emails = None  # Generate all possible variations
elif max_emails is not None:
    max_emails = int(max_emails)

emails = list(generate_dot_emails(username, max_emails))

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
