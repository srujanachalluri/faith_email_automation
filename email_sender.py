
import pandas as pd
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Email credentials
sender_email = "srujanachalluri@gmail.com"
password = "gitalyiqbxafrica"
receiver_email = "srujanachalluri@gmail.com"

# Read CSV
df = pd.read_csv("faith_email_verses.csv")

# Loop through rows
for index, row in df.iterrows():
    name = row["Name"]
    recipient = row["Email"]
    verse = row["Verse"]
    theme = row["Theme"]
    image_path = row["ImagePath"]

    # Create email message
    msg = MIMEMultipart("related")
    msg["Subject"] = f"{theme} - A Daily Blessing for You"
    msg["From"] = sender_email
    msg["To"] = recipient


    # Email HTML body with inline image (Content-ID must match)
    html = f"""
    <html>
      <body style = "background-color: beige; font-size: 20px;">
        <h2 style="color:#2e6c80;">Dear {name},</h2>
        <p><strong>Bible Verse:</strong> {verse}</p>
        <p><em>Theme:</em> {theme}</p>
        <p style="color: navy">Have a blessed day! ✨</p>

            <p style="margin-top: 15px;">
                📘 View related content on <a href="https://www.canva.com/design/DAGuefWJCb4/BAYt58iD4qclEPAprPpbfQ/watch?utm_content=DAGuefWJCb4&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hb28b394a2b" target="_blank" 
                style="color:#1a0dab;">Canvas:- Link to View Full Post <br/> @srujanachalluri</a>
            </p>
      </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    # Attach image
    try:
        with open(image_path, 'rb') as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-ID', '<image1>')
            img.add_header("Content-Disposition", "inline", filename=os.path.basename(image_path))
            msg.attach(img)
    except FileNotFoundError:
        print(f"❌ Image not found: {image_path}")
        continue

     # Send email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.send_message(msg)
            print(f"✅ Email sent to {name} ({recipient})")
    except Exception as e:
        print(f"❌ Failed to send email to {recipient}: {e}")
