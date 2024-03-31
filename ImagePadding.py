import os
import cv2
import numpy as np

# Input and output directories
path = "/GitHub/AutoRadAI/Padd/DataOrig"
dest_path = "/GitHub/AutoRadAI/Padd/DataSqr"

# Ensure the output directory exists
os.makedirs(dest_path, exist_ok=True)

for img_name in os.listdir(path):
    img_path = os.path.join(path, img_name)
    
    # Read the image
    image = cv2.imread(img_path)
    
    if image is not None:
        # Get the original dimensions
        original_height, original_width = image.shape[:2]
        
        # Determine which side (height or width) is larger
        larger_side = max(original_height, original_width)
        
        # Create a square canvas with the original resolution
        square_canvas = np.zeros((larger_side, larger_side, 3), dtype=np.uint8)
        
        # Calculate the coordinates to paste the original image
        y1 = (larger_side - original_height) // 2
        y2 = y1 + original_height
        x1 = (larger_side - original_width) // 2
        x2 = x1 + original_width
        
        # Copy the original image onto the square canvas
        square_canvas[y1:y2, x1:x2] = image
        
        # Save the squared image with the same name and format
        dest_image_path = os.path.join(dest_path, img_name)
        cv2.imwrite(dest_image_path, square_canvas)
        
        # Print the final resolution and dimensions
        final_height, final_width = square_canvas.shape[:2]
        print(f"Image {img_name}: Resolution: {final_width} x {final_height}, Dimensions: {final_width} × {final_height}")
    else:
        print(f"Unable to read image: {img_name}")

print("Cropping complete. Images are now square without resizing.")
