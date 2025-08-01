import streamlit as st
from utils.sheet_reader import fetch_employee_data
from utils.image_tools import load_image, apply_rounded_edges
from utils.email_sender import send_email
from PIL import Image, ImageDraw, ImageFont
import qrcode
from datetime import datetime
import os

# Layout
st.set_page_config(page_title="New Employee Entry", layout="centered")
st.title("New Employee Entry Received")

# Load templates
front_template = Image.open("assets/ip-front.jpg")
back_template = Image.open("assets/ip-back.jpg")

# Fonts
font_xlarge = ImageFont.truetype("assets/fonts/Arial-Black.ttf", 50)
font_large = ImageFont.truetype("assets/fonts/Arial-Bold.ttf", 50)
font_medium = ImageFont.truetype("assets/fonts/Arial-Bold.ttf", 35)
font_small = ImageFont.truetype("assets/fonts/Arial.ttf", 30)

# Load latest employee data
sheet_name = "EmployeeData"
worksheet_name = "Sheet1"
data = fetch_employee_data(sheet_name, worksheet_name)

if not data:
    st.warning("No employee entries found.")
else:
    emp = data[-1]  # Latest row
    name = emp["Name"]
    designation = emp["Designation"]
    emp_id = emp["Employee ID"]
    email = emp["Email ID"]
    phone = str(emp["Phone"])
    cnic = emp["CNIC"]
    blood_group = emp["Blood Group"]
    doj = emp["Date of Joining"]
    image_url = emp["Image File"]

    formatted_date = datetime.strptime(doj, "%d-%m-%Y").strftime("%d-%m-%Y")

    st.success(f"✅ New Entry: {name} ({designation})")
    st.write(f"**Employee ID:** {emp_id}")
    st.write(f"**Email:** {email}")
    st.write(f"**Phone:** {phone}")
    st.write(f"**CNIC:** {cnic}")
    st.write(f"**Date of Joining:** {formatted_date}")
    st.markdown("---")

    # Generate card images (not shown to user)
    emp_img = load_image(image_url).resize((280, 280))
    emp_img = apply_rounded_edges(emp_img, radius=30)

    # QR code
    qr_data = f"Name: {name}\nDesignation: {designation}\nID: {emp_id}\nEmail: {email}\nPhone: {phone}\nWebsite: https://ipath.tech"
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill="black", back_color="white").resize((370, 370))

    # Create front card
    front = front_template.copy()
    draw_front = ImageDraw.Draw(front)
    front.paste(emp_img, (210, 240), emp_img)

    name_width, _ = draw_front.textbbox((0, 0), name, font=font_xlarge)[2:4]
    draw_front.text(((front.width - name_width)//2, 530), name, fill="black", font=font_xlarge)

    designation_width, _ = draw_front.textbbox((0, 0), designation, font=font_medium)[2:4]
    draw_front.text(((front.width - designation_width)//2, 590), designation, fill="black", font=font_medium)

    draw_front.text((380, 660), emp_id, fill="black", font=font_small)
    draw_front.text((350, 710), formatted_date, fill="black", font=font_small)
    draw_front.text((300, 760), cnic, fill="black", font=font_small)

    # Create back card
    back = back_template.copy()
    draw_back = ImageDraw.Draw(back)
    back.paste(qr_img, (160, 430))
    draw_back.text((150, 300), blood_group, fill="black", font=font_large)

    # Save both
    os.makedirs("output", exist_ok=True)
    front_path = f"output/{emp_id}_front.png"
    back_path = f"output/{emp_id}_back.png"
    front.save(front_path)
    back.save(back_path)

    # Send to HR
    try:
        send_email(
            subject=f"New Employee Card: {name}",
            body=f"""New card generated:

Name: {name}
Designation: {designation}
Employee ID: {emp_id}
CNIC: {cnic}
Phone: {phone}
Email: {email}
Date of Joining: {formatted_date}
""",
            attachments=[front_path, back_path]
        )
        st.success("Card sent to HR successfully!")
    except Exception as e:
        st.error(f"Email sending failed: {e}")
