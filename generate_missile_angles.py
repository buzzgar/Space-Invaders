from PIL import Image, ImageSequence
import os

# Load the animated GIF
image = Image.open("assets/laser.gif")

# Rotation bounds and step
start_angle = -90
end_angle = 90
step = 1

# Output directory
output_dir = "assets/missile/"
os.makedirs(output_dir, exist_ok=True)

# Loop over each rotation angle
for angle in range(start_angle, end_angle + 1, step):
    # Subdirectory for each rotation angle
    angle_dir = os.path.join(output_dir, f"angle_{angle}")
    os.makedirs(angle_dir, exist_ok=True)

    # Iterate through all frames
    for i, frame in enumerate(ImageSequence.Iterator(image)):
        # Convert frame to RGBA for transparency
        frame = frame.convert("RGBA")

        # Rotate the frame
        rotated = frame.rotate(angle, expand=True)

        # Optional: Paste on transparent background to clean up edges
        bg = Image.new("RGBA", rotated.size, (0, 0, 0, 0))
        bg.paste(rotated, (0, 0), rotated)

        # Save the rotated frame
        filename = f"frame_{i:03}.png"
        bg.save(os.path.join(angle_dir, filename))

    print(f"Saved frames for angle {angle}° in folder: {angle_dir}")