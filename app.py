from flask import Flask, request, render_template, redirect, url_for, flash
from google_images_search import GoogleImagesSearch
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from requests.exceptions import SSLError, RequestException

# Set up your Google Custom Search API credentials
api_key = 'AIzaSyC6br5zLu_Pc-AWjYSci9-BkCslLpQJGdM'
cx = 'f4fdeeeadc50849b6'
gis = GoogleImagesSearch(api_key, cx)

app = Flask(__name__)
app.secret_key = '1bab65dff2dd6d51219a177ad77e1d6257efc2543aef410b'

# Email credentials
sender_email = "bhoomsie1@gmail.com"
sender_password = "wpvt wwch ursi yzqi" # Replace this with an app-specific password

# Directory to save downloaded images
output_folder = "images"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to download images
def download_images(search_term, num_images, output_folder):
    search_params = {
        'q': search_term,
        'num': num_images,
        'safe': 'high',
        'fileType': 'jpg|png',
        'imgType': 'photo',
        'imgSize': 'MEDIUM'
    }
    try:
        gis.search(search_params=search_params, path_to_dir=output_folder)
        print(f"Downloaded {num_images} images of {search_term} to {output_folder}")
    except Exception as e:
        print(f"Error downloading images: {e}")

# Function to send an email with attachments
def send_email_with_attachments(recipient_email, output_folder):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = 'Your Images'

    # Attach files from output_folder
    for filename in os.listdir(output_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            file_path = os.path.join(output_folder, filename)
            with open(file_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={filename}')
                msg.attach(part)

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

    print("Email sent successfully!")

# Routes
@app.route('/')
def index():
    return render_template('index.html')

import shutil  # Import shutil to help with removing the directory

# Function to clear the output folder
def clear_output_folder(output_folder):
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)  # Delete the entire directory
    os.makedirs(output_folder)  # Recreate an empty directory

@app.route('/download_images', methods=['POST'])
def download_images_route():
    recipient_email = request.form.get('recipient_email')
    search_term = request.form.get('search_term')
    num_images = request.form.get('num_images', type=int)

    if not recipient_email or not search_term or not num_images:
        return "Please fill in all required fields", 400

    # Clear the output folder to avoid mixing images from previous searches
    clear_output_folder(output_folder)

    # Download images
    download_images(search_term, num_images, output_folder)

    # Send images via email
    send_email_with_attachments(recipient_email, output_folder)

    # Redirect to success page after sending email
    return redirect(url_for('success'))

# Success page route
@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == "__main__":
    app.run(debug=True)
