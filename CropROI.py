import os
import cv2

# Specify input and output directories
input_dir = '/GitHub/AutoRadAI/Crop/Distinct'
output_dir = '/GitHub/AutoRadAI/Crop/CropImage'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Process each image in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.png'):
        # Read the image
        image_path = os.path.join(input_dir, filename)
        image = cv2.imread(image_path)

        # Resize the image to 512x512
        target_size = (768, 768)
        resized_image = cv2.resize(image, target_size)

        # Calculate the cropping boundaries
        crop_x1 = (resized_image.shape[1] - 512) // 2
        crop_x2 = crop_x1 + 512
        crop_y1 = (resized_image.shape[0] - 512) // 2
        crop_y2 = crop_y1 + 512

        # Crop the square from the resized image
        cropped_image = resized_image[crop_y1:crop_y2, crop_x1:crop_x2]

        # Save the cropped image as a new image
        output_path = os.path.join(output_dir, filename)
        cv2.imwrite(output_path, cropped_image)

        # Print the resolution of the cropped image
        print(f"Resolution of {filename}: {cropped_image.shape[1]}x{cropped_image.shape[0]}")