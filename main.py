import os
from PIL import Image, ImageDraw, ImageFont
from utils.sheet_reader import fetch_employee_data
from utils.image_tools import load_image
import qrcode
from datetime import datetime

# Output folder
os.makedirs("output", exist_ok=True)

# Templates
front_template = Image.open("assets/ip-front.jpg")
back_template = Image.open("assets/ip-back.jpg")

# Fonts
font_xlarge = ImageFont.truetype("assets/fonts/Arial-Black.ttf", 50)
font_large = ImageFont.truetype("assets/fonts/Arial-Bold.ttf", 50)
font_medium = ImageFont.truetype("assets/fonts/Arial-Bold.ttf", 35)
font_small = ImageFont.truetype("assets/fonts/Arial.ttf", 30)

# Google Sheet details
sheet_name = "Employee Cards"
worksheet_name = "Sheet1"

# Fetch all rows from Google Sheet
employees = fetch_employee_data(sheet_name, worksheet_name)

def apply_rounded_edges(image, radius):
    image = image.convert("RGBA")
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)
    rounded_image = Image.new("RGBA", image.size)
    rounded_image.paste(image, mask=mask)
    return rounded_image

# Generate cards
for emp in employees:
    try:
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

        # Load and round employee image
        emp_img = load_image(image_url).resize((280, 280))
        emp_img = apply_rounded_edges(emp_img, radius=30)

        # Generate QR code
        qr_data = f"Name: {name}\nDesignation: {designation}\nID: {emp_id}\nEmail: {email}\nPhone: {phone}\nWebsite: https://ipath.tech"
        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill="black", back_color="white").resize((370, 370))

        # Front card
        front_card = front_template.copy()
        draw_front = ImageDraw.Draw(front_card)
        front_card.paste(emp_img, (210, 240), emp_img)

        name_width, _ = draw_front.textbbox((0, 0), name, font=font_xlarge)[2:4]
        name_x = (front_card.width - name_width) // 2
        draw_front.text((name_x, 530), name, fill="black", font=font_xlarge)

        designation_width, _ = draw_front.textbbox((0, 0), designation, font=font_medium)[2:4]
        designation_x = (front_card.width - designation_width) // 2
        draw_front.text((designation_x, 590), designation, fill="black", font=font_medium)

        draw_front.text((380, 660), emp_id, fill="black", font=font_small)
        draw_front.text((350, 710), formatted_date, fill="black", font=font_small)
        draw_front.text((300, 760), cnic, fill="black", font=font_small)

        # Back card
        back_card = back_template.copy()
        draw_back = ImageDraw.Draw(back_card)
        back_card.paste(qr_img, (160, 430))
        draw_back.text((150, 300), blood_group, fill="black", font=font_large)

        # Save both
        front_path = f"output/{emp_id}_front.png"
        back_path = f"output/{emp_id}_back.png"

        front_card.save(front_path)
        back_card.save(back_path)

        print(f"[✔] Card generated for: {name}")

    except Exception as e:
        print(f"[❌] Failed for {emp.get('Name', 'Unknown')}: {e}")
