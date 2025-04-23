from PIL import Image

# Open the original image (which has transparency, like a PNG)
image = Image.open("assets/shield.png")

# Resize the image (this will maintain transparency)
resized = image.resize((150, 150))

# Save the image back to PNG to preserve transparency
resized.save("assets/shield_resized.png", format="PNG")






