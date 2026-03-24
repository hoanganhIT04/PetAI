import os
import json
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.applications import MobileNetV2
from sklearn.utils.class_weight import compute_class_weight

# ================== PATH ==================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DATASET_PATH = os.path.join(BASE_DIR, "frontend", "public", "assets", "data", "data_model_2")
CSV_PATH     = os.path.join(BASE_DIR, "ai", "data", "metadata.csv")
MODEL_PATH   = os.path.join(BASE_DIR, "ai","model","model_v2.h5")
LABEL_PATH   = os.path.join(BASE_DIR, "ai","label", "label_v2.json")

# ================== CONFIG ==================
IMG_SIZE      = (224, 224)
BATCH_SIZE    = 16

# ================== LOAD CSV ==================
df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
df = df.dropna(subset=["tên giống loài"])

ordered_classes = (
    df["tên giống loài"]
    .astype(str)
    .str.strip()
    .str.lower()
    .drop_duplicates()
    .tolist()
)

print(f"Classes từ CSV: {len(ordered_classes)}")

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

val_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_generator = train_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training",
    shuffle=True,
    # classes=ordered_classes
)
print("Num classes:", train_generator.num_classes)
print(train_generator.class_indices)

val_generator = val_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation",
    shuffle=False,
    # classes=ordered_classes
)

# ================== CHECK UNKNOWN ==================
if "unknown" not in train_generator.class_indices:
    print("Không có class unknown → SAI DATASET")
    exit()
else:
    print("Found UNKNOWN class")

# ================== CLASS WEIGHT ==================
classes = np.unique(train_generator.classes)
weights = compute_class_weight(
    class_weight='balanced',
    classes=classes,
    y=train_generator.classes
)
class_weights = dict(enumerate(weights))

print("\nClass weights:")
for k, v in class_weights.items():
    print(k, v)

# ================== LABEL MAP ==================
label_mapping = train_generator.class_indices
idx_to_label = {str(v): k for k, v in label_mapping.items()}

with open(LABEL_PATH, "w", encoding="utf-8") as f:
    json.dump(idx_to_label, f, ensure_ascii=False, indent=4)

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
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.4),
    layers.Dense(train_generator.num_classes, activation="softmax")
])

# giảm overconfidence
loss_fn = tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.1)

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss=loss_fn,
    metrics=["accuracy"]
)

callbacks = [
    EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True),
    ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3, min_lr=1e-7)
]

# ================== TRAIN PHASE 1 ==================
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=15,
    callbacks=callbacks,
    class_weight=class_weights
)

# ================== FINE-TUNE ==================
for layer in base_model.layers[-20:]:
    layer.trainable = True

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
    loss=loss_fn,
    metrics=["accuracy"]
)

history_ft = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=15,
    callbacks=callbacks,
    class_weight=class_weights
)

# ================== SAVE ==================
model.save(MODEL_PATH)
print("Model saved")

# ================== TUNE THRESHOLD T ==================
print("\TUNING THRESHOLD...")

y_true = val_generator.classes
y_pred_prob = model.predict(val_generator)
max_probs = np.max(y_pred_prob, axis=1)
y_pred = np.argmax(y_pred_prob, axis=1)

best_T = 0
best_acc = 0

for T in np.arange(0.2, 0.9, 0.05):
    mask = max_probs >= T
    if np.sum(mask) == 0:
        continue

    acc = np.mean(y_pred[mask] == y_true[mask])

    if acc > best_acc:
        best_acc = acc
        best_T = T

print(f"Best Threshold T = {best_T:.2f} | Acc = {best_acc:.4f}")

# ================== RESULT ==================
val_loss, val_acc = model.evaluate(val_generator, verbose=0)

train_acc = history_ft.history["accuracy"][-1]  # phase fine-tune
gap = train_acc - val_acc

print("\n" + "=" * 60)
print("KẾT QUẢ CUỐI")

print(f"Train Acc: {train_acc * 100:.2f}%")
print(f"Val Acc:   {val_acc * 100:.2f}%")
print(f"Gap:       {gap * 100:.2f}%")

# thêm threshold vào nhưng không phá format
print(f"Best Threshold (T): {best_T:.2f}")

if gap < 0.08:
    print("ĐÁNH GIÁ: TỐT (gap thấp)")
elif gap < 0.15:
    print("ĐÁNH GIÁ: ỔN (gap chấp nhận)")
else:
    print("ĐÁNH GIÁ: OVERFITTING")

print("=" * 60)