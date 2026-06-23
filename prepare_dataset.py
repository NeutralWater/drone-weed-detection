import os
import random
import shutil

SOURCE_FOLDER = r"C:\Users\d\Downloads\archive"
OUTPUT_FOLDER = r"C:\Users\d\Desktop\weed-ai-dataset"

WEED_CLASSES = [
    "Black-grass",
    "Charlock",
    "Common Chickweed"
]

NOT_WEED_CLASSES = [
    "Common wheat",
    "Maize",
    "Sugar beet"
]

IMAGES_PER_CLASS = 300
TRAIN_SPLIT = 0.8

random.seed(42)

for split in ["train", "val"]:
    for label in ["weed", "not_weed"]:
        os.makedirs(os.path.join(OUTPUT_FOLDER, split, label), exist_ok=True)

def copy_images(class_names, label):
    for class_name in class_names:
        class_path = os.path.join(SOURCE_FOLDER, class_name)

        images = [
            file for file in os.listdir(class_path)
            if file.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

        random.shuffle(images)
        images = images[:IMAGES_PER_CLASS]

        split_index = int(len(images) * TRAIN_SPLIT)

        for index, image_name in enumerate(images[:split_index]):
            shutil.copy2(
                os.path.join(class_path, image_name),
                os.path.join(
                    OUTPUT_FOLDER,
                    "train",
                    label,
                    f"{class_name}_{index}_{image_name}"
                )
            )

        for index, image_name in enumerate(images[split_index:]):
            shutil.copy2(
                os.path.join(class_path, image_name),
                os.path.join(
                    OUTPUT_FOLDER,
                    "val",
                    label,
                    f"{class_name}_{index}_{image_name}"
                )
            )

copy_images(WEED_CLASSES, "weed")
copy_images(NOT_WEED_CLASSES, "not_weed")

print("Done!")
print("Dataset created at:", OUTPUT_FOLDER)