from PIL import Image

# Open the image file
image = Image.open("bg.png")

# Resize the image to the desired size (e.g., 32x32 pixels)
image = image.resize((32, 32))

# Save the resized image
image.save("resized_image.png")


"""from PIL import Image

# Open the original image
original_image = Image.open("bg.png")

# Define the target size
target_size = (450,270 )  # Example target size

# Resize the image while maintaining aspect ratio
original_image.thumbnail(target_size)

# Save the resized image
original_image.save("resized_image.png")"""

