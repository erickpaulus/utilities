
import fitz  # PyMuPDF
from PIL import Image
import io

# --- Settings ---
pdf_path = rf"input.pdf"           # Your PDF file
image_path = rf"image.jpg"         # Image to add (PNG or JPG)
output_pdf = "output.pdf"          # Result file
page_number = 1
x, y = 400, 350  # position in points (from bottom-left)
scale_percent = 70  # scale image to 50% of original size

# --- Open PDF and image ---
doc = fitz.open(pdf_path)
page = doc[page_number]

image = Image.open(image_path)

# Calculate new size keeping aspect ratio
orig_width, orig_height = image.size
new_width = int(orig_width * scale_percent / 100)
new_height = int(orig_height * scale_percent / 100)

# Resize image
image = image.resize((new_width, new_height))

# Convert to bytes
img_buffer = io.BytesIO()
image.save(img_buffer, format="PNG")
img_bytes = img_buffer.getvalue()

# Adjust Y coordinate (PyMuPDF origin bottom-left)
page_height = page.rect.height
adjusted_y = page_height - y

# Define rectangle for image placement
rect = fitz.Rect(x, adjusted_y, x + new_width, adjusted_y + new_height)

# Insert image
page.insert_image(rect, stream=img_bytes)
rect = page.rect

print(f"Page size: width={rect.width} pt, height={rect.height} pt")
# Save output
doc.save(output_pdf)
doc.close()
print(f"✅ Image inserted on page {page_number + 1} at ({x},{y}) scaled to {scale_percent}%")
