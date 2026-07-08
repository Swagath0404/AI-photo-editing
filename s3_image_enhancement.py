import tensorflow as tf
import cv2
import numpy as np
import os

IMG_SIZE = 128

# Load trained model
model = tf.keras.models.load_model("ai_photo_editor.h5")

# Load test image
img_path = "test_images/test.jpg"
img = cv2.imread(img_path)

if img is None:
    print("Error: Image not found")
    exit()

img_resized = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
img_norm = img_resized / 255.0
img_input = np.expand_dims(img_norm, axis=0)

# Predict enhanced image
output = model.predict(img_input)[0]
output = (output * 255).astype(np.uint8)

# Save output image
os.makedirs("output", exist_ok=True)
cv2.imwrite("output/enhanced_test.jpg", output)

print("Enhanced image saved in output/enhanced_test.jpg")
