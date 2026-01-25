import os
import json
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.applications import MobileNetV2

# ================== PATH ==================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DATASET_PATH = os.path.join(BASE_DIR, "frontend", "public", "assets", "dog_images")
CSV_PATH     = os.path.join(BASE_DIR, "ai", "data", "dog.csv")
MODEL_PATH   = os.path.join(BASE_DIR, "ai", "dog.h5")
LABEL_PATH   = os.path.join(BASE_DIR, "ai", "dog_label.json")

# ================== CONFIG ==================
IMG_SIZE      = (224, 224)
BATCH_SIZE    = 16
# EPOCHS        = 30
# LEARNING_RATE = 2e-4

# ================== LOAD & CLEAN CSV ==================
try:
    df = pd.read_csv(CSV_PATH)
    df = df.dropna(subset=["tên giống loài"])

    ordered_classes = (
        df["tên giống loài"]
        .astype(str)
        .str.strip()
        .str.lower()
        .drop_duplicates()
        .tolist()
    )

    print(f"Đã load {len(ordered_classes)} giống từ CSV")
    print("Mapping preview:")
    for i, name in enumerate(ordered_classes[:5]):
        print(f"  {i}: {name}")

except Exception as e:
    print("LỖI CSV:", e)
    exit()


# ================== DATA GENERATOR ==================
train_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.15,
    horizontal_flip=True,
    brightness_range=[0.85, 1.15],
    fill_mode="nearest"
)

val_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training",
    shuffle=True,
    classes=ordered_classes
)

val_generator = val_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation",
    shuffle=False,
    classes=ordered_classes
)

# ================== LABEL MAP ==================
label_mapping = train_generator.class_indices
idx_to_label = {str(v): k for k, v in label_mapping.items()}

with open(LABEL_PATH, "w", encoding="utf-8") as f:
    json.dump(idx_to_label, f, ensure_ascii=False, indent=4)

num_classes = train_generator.num_classes
print(f"Classes: {num_classes}")
print(f"Train samples: {train_generator.samples}")
print(f"Val samples: {val_generator.samples}")

# ================== MODEL ==================
base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(*IMG_SIZE, 3)
)

# ===== PHASE 1: FEATURE EXTRACTION =====
for layer in base_model.layers:
    layer.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.4),
    layers.Dense(train_generator.num_classes, activation="softmax")
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

callbacks_phase1 = [
    EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True,
        verbose=1
    )
]

history_phase1 = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=15,
    callbacks=callbacks_phase1
)

# ===== PHASE 2: FINE-TUNING =====
for layer in base_model.layers[-20:]:
    layer.trainable = True

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

callbacks_phase2 = [
    EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True,
        verbose=1
    ),
    ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=3,
        min_lr=1e-7,
        verbose=1
    )
]

history_phase2 = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=20,
    callbacks=callbacks_phase2
)

# ================== TRAIN ==================
print("\nBẮT ĐẦU TRAINING\n")

model.save(MODEL_PATH)
print(f"\nĐã lưu model: {MODEL_PATH}")

# ================== RESULT ==================
val_loss, val_acc = model.evaluate(val_generator, verbose=0)
train_acc = history_phase2.history["accuracy"][-1]
gap = train_acc - val_acc

print("\n" + "=" * 60)
print("KẾT QUẢ CUỐI")
print(f"Train Acc: {train_acc * 100:.2f}%")
print(f"Val Acc:   {val_acc * 100:.2f}%")
print(f"Gap:       {gap * 100:.2f}%")

if gap < 0.08:
    print("ĐÁNH GIÁ: TỐT (gap thấp)")
elif gap < 0.15:
    print("ĐÁNH GIÁ: ỔN (gap chấp nhận)")
else:
    print("ĐÁNH GIÁ: OVERFITTING")

print("=" * 60)
