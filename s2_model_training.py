# s2_model_training.py
# ML Photo Enhancement using U-Net + Data Generator (RAM safe)

import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, concatenate
from tensorflow.keras.models import Model

# ---------------- PARAMETERS ----------------
IMG_SIZE = 128
BATCH_SIZE = 2
EPOCHS = 5

INPUT_FOLDER = "dataset/input"
ENHANCED_FOLDER = "dataset/enhanced"
MODEL_SAVE_PATH = "ai_photo_editor.h5"

# ---------------- U-NET MODEL ----------------
def unet_model(input_size=(IMG_SIZE, IMG_SIZE, 3)):
    inputs = Input(input_size)

    # Encoder
    c1 = Conv2D(64, 3, activation='relu', padding='same')(inputs)
    c1 = Conv2D(64, 3, activation='relu', padding='same')(c1)
    p1 = MaxPooling2D()(c1)

    c2 = Conv2D(128, 3, activation='relu', padding='same')(p1)
    c2 = Conv2D(128, 3, activation='relu', padding='same')(c2)
    p2 = MaxPooling2D()(c2)

    # Bottleneck
    c3 = Conv2D(256, 3, activation='relu', padding='same')(p2)
    c3 = Conv2D(256, 3, activation='relu', padding='same')(c3)

    # Decoder
    u4 = UpSampling2D()(c3)
    u4 = concatenate([u4, c2])
    c4 = Conv2D(128, 3, activation='relu', padding='same')(u4)
    c4 = Conv2D(128, 3, activation='relu', padding='same')(c4)

    u5 = UpSampling2D()(c4)
    u5 = concatenate([u5, c1])
    c5 = Conv2D(64, 3, activation='relu', padding='same')(u5)
    c5 = Conv2D(64, 3, activation='relu', padding='same')(c5)

    outputs = Conv2D(3, 1, activation='sigmoid')(c5)

    return Model(inputs, outputs)

# ---------------- DATA GENERATOR ----------------
def data_generator(input_folder, enhanced_folder, batch_size=BATCH_SIZE, img_size=IMG_SIZE):
    input_images = sorted(os.listdir(input_folder))
    enhanced_images = sorted(os.listdir(enhanced_folder))

    while True:
        for i in range(0, len(input_images), batch_size):
            X, Y = [], []

            for inp, enh in zip(
                input_images[i:i+batch_size],
                enhanced_images[i:i+batch_size]
            ):
                img_in = cv2.imread(os.path.join(input_folder, inp))
                img_enh = cv2.imread(os.path.join(enhanced_folder, enh))

                if img_in is None or img_enh is None:
                    continue

                img_in = cv2.resize(img_in, (img_size, img_size))
                img_enh = cv2.resize(img_enh, (img_size, img_size))

                X.append(img_in / 255.0)
                Y.append(img_enh / 255.0)

            if len(X) > 0:
                yield np.array(X, dtype=np.float32), np.array(Y, dtype=np.float32)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    print("🚀 Starting ML Photo Enhancement Training")

    model = unet_model()
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.summary()

    train_gen = data_generator(INPUT_FOLDER, ENHANCED_FOLDER)

    steps_per_epoch = len(os.listdir(INPUT_FOLDER)) // BATCH_SIZE

    model.fit(
        train_gen,
        steps_per_epoch=steps_per_epoch,
        epochs=EPOCHS
    )

    model.save(MODEL_SAVE_PATH)
    print(f"✅ Model saved as {MODEL_SAVE_PATH}")
