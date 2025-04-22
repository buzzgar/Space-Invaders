from PIL import Image
import os

def gif_to_frames(gif_path, output_folder):
    # Open the GIF file
    with Image.open(gif_path) as im:
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        frame = 0
        try:
            while True:
                # Save each frame as a PNG
                im.save(f"{output_folder}/frame_{frame:03d}.png", format="PNG")
                frame += 1
                im.seek(im.tell() + 1)  # Move to next frame
        except EOFError:
            print(f"Done! Extracted {frame} frames to '{output_folder}'.")

# Example usage
gif_to_frames("assets/astro-background.gif", "astro-background")
