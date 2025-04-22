import cv2
import utils.utils

# Load image in color (BGR) mode
im = cv2.imread("assets/pngegg.png", cv2.IMREAD_COLOR)

# Resize to 54x54
im = cv2.resize(im, (54, 54))

# Optional: save resized image
cv2.imwrite("test.png", im)

lines = []
for i in range(im.shape[0]):
    line = []
    for j in range(im.shape[1]):
        b, g, r = im[i, j]  # OpenCV uses BGR order
        rgb = (r, g, b)     # Convert to RGB if needed
        line.append(str(utils.utils.rgb_to_int(rgb)))
    lines.append(",".join(line))

# Save to text file
with open("assets/tie-fighter.txt", "w") as f:
    f.write("\n".join(lines))
