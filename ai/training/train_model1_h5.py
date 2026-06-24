import os
import json
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.applications import MobileNetV2
from PIL import ImageFile

# ✅ FIX 1: cho phép load ảnh lỗi
ImageFile.LOAD_TRUNCATED_IMAGES = True

# ✅ FIX 2: chạy tuần tự tránh lỗi random
tf.data.experimental.enable_debug_mode()

# ================== PATH ==================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DATASET_PATH = os.path.join(BASE_DIR, "frontend", "public", "assets", "data", "data_model_1")
MODEL_PATH   = os.path.join(BASE_DIR, "ai", "model", "model_binary.h5")   
LABEL_PATH   = os.path.join(BASE_DIR, "ai", "label", "label_binary_h5.json")

# ================== CONFIG ==================
IMG_SIZE   = (224, 224)
BATCH_SIZE = 16

# ================== DATA ==================
train_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=15,
    zoom_range=0.1,
    horizontal_flip=True
)

val_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    subset="training",
    shuffle=True
)

val_generator = val_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    subset="validation",
    shuffle=False
)

# ================== LABEL ==================
label_mapping = train_generator.class_indices
idx_to_label = {str(v): k for k, v in label_mapping.items()}

with open(LABEL_PATH, "w") as f:
    json.dump(idx_to_label, f, indent=4)

print("Label map:", idx_to_label)

# ================== MODEL ==================
base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(*IMG_SIZE, 3)
)

for layer in base_model.layers:
    layer.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.BatchNormalization(),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.4),
    layers.Dense(1, activation="sigmoid")
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

# ================== CALLBACK ==================
callbacks = [
    EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True
    ),
    ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=3,
        min_lr=1e-6
    )
]

# ================== TRAIN ==================
print("\START TRAINING...\n")

model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=30,
    callbacks=callbacks
)

# ================== SAVE ==================
model.save(MODEL_PATH, save_format="h5")  
print("Saved model (.h5)!")

# ================== EVAL ==================
val_loss, val_acc = model.evaluate(val_generator)
print(f"Val Acc: {val_acc*100:.2f}%")