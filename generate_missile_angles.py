from PIL import Image
import os

# Load the image
image = Image.open("assets/laser.gif")  # Replace with your image filename

# Rotation bounds and step
start_angle = -90
end_angle = 90
step = 1

# Output directory
output_dir = "assets/missile/"
os.makedirs(output_dir, exist_ok=True)

# Rotate and save images
for angle in range(start_angle, end_angle + 1, step):
    rotated = image.rotate(angle, expand=True, fillcolor=(0, 0, 0))  # expand keeps full image
    filename = f"rotated_{angle}.png"
    rotated.save(os.path.join(output_dir, filename))
    print(f"Saved: {filename}")
