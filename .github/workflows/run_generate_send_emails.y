name: Run Generate and Send Emails

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests
      
      - name: Run generate and send emails script
        run: python generate_send_emails.py
        env:
          username: ${{ secrets.GMAIL_USERNAME }}
          webhook_url: ${{ secrets.DISCORD_WEBHOOK_URL }}
