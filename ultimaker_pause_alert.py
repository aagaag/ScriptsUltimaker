import os
import base64
import smtplib
from email.mime.text import MIMEText

# Function to encode and save credentials
def save_credentials(user_id, password, file_path):
    encoded_user_id = base64.b64encode(user_id.encode()).decode()
    encoded_password = base64.b64encode(password.encode()).decode()
    with open(file_path, 'w') as file:
        file.write(f"{encoded_user_id}\n{encoded_password}")

# Function to read and decode credentials
def read_credentials(file_path):
    with open(file_path, 'r') as file:
        encoded_user_id, encoded_password = file.read().split('\n')
        user_id = base64.b64decode(encoded_user_id.encode()).decode()
        password = base64.b64decode(encoded_password.encode()).decode()
        return user_id, password

# Main script
credentials_file = 'credentials.txt'

# Check if credentials file exists
if not os.path.exists(credentials_file):
    user_id = input("Enter your user ID: ")
    password = input("Enter your password: ")
    save_credentials(user_id, password, credentials_file)

user_id, password = read_credentials(credentials_file)

# Email sending logic using SMTP_SSL for secure connection
recipient = "adriano.aguzzi@usz.ch"
subject = "Test Email"
body = "This is a test email sent from Python."

message = MIMEText(body)
message['From'] = user_id
message['To'] = recipient
message['Subject'] = subject

# Connect to the SMTP server using SSL
server = smtplib.SMTP_SSL('smtpauths.bluewin.ch', 465)
server.login(user_id, password)
server.sendmail(user_id, recipient, message.as_string())
server.quit()

print("Email sent successfully!")
