from PIL import Image, ImageDraw
import requests
from io import BytesIO

# 🟡 Image URL se image load karna
def load_image(url):
    # Agar Google Drive sharing link diya gaya hai
    if "drive.google.com" in url and "uc?export=download" not in url:
        # Convert to direct download URL
        try:
            file_id = url.split("/d/")[1].split("/")[0]
            url = f"https://drive.google.com/uc?export=download&id={file_id}"
        except:
            raise ValueError("❌ Invalid Google Drive URL format")

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("❌ Failed to load image from URL")
    
    return Image.open(BytesIO(response.content)).convert("RGBA")


# 🟢 Rounded edges apply karna
def apply_rounded_edges(image, radius):
    image = image.convert("RGBA")
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)
    rounded_image = Image.new("RGBA", image.size)
    rounded_image.paste(image, mask=mask)
    return rounded_image
