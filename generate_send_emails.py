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

save_to_file = os.getenv('SAVE_TO_FILE', 'true').lower() == 'true'
send_to_discord = os.getenv('SEND_TO_DISCORD', 'true').lower() == 'true'
send_as_message = os.getenv('SEND_AS_MESSAGE', 'true').lower() == 'true'

filename = None

if save_to_file:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{username}@gmail.com_emails_{timestamp}.txt"

    with open(filename, 'w') as f:
        for email in emails:
            f.write(email + '\n')

    print(f"Emails saved to {filename}")

def send_emails_to_discord(content, webhook_url):
    payload = {
        'content': content
    }

    response = requests.post(webhook_url, json=payload)
    if response.status_code == 204:
        print("Emails sent to Discord successfully!")
    else:
        print(f"Failed to send emails to Discord. Status code: {response.status_code}")

def send_file_to_discord(filename, webhook_url):
    with open(filename, 'rb') as f:
        files = {
            'file': (filename, f, 'text/plain')
        }
        response = requests.post(webhook_url, files=files)
        if response.status_code == 204:
            print(f"File {filename} sent to Discord successfully!")
        else:
            print(f"Failed to send file {filename} to Discord. Status code: {response.status_code}")

if send_to_discord:
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if not webhook_url:
        raise ValueError("DISCORD_WEBHOOK_URL environment variable is not set")
    
    if save_to_file and filename:
        send_file_to_discord(filename, webhook_url)
    
    if send_as_message:
        send_emails_to_discord('\n'.join(emails), webhook_url)
