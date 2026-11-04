# from pathlib import Path
# from ultralytics import YOLO

# DATASET = "dataset/data.yaml"
# MODEL = "yolo11n.pt"
# OUTPUT = Path(__file__).resolve().parent / "workshop_runs" / "detect"
# model = YOLO(MODEL)

# model.train(
#     data=DATASET,
#     epochs=??,
#     imgsz=??,
#     batch=??,
#     project=OUTPUT,
#     # device="auto", # for Nvidia GPU users (must have installed pytorch with CUDA)
#     device="cpu", # for CPU users
#     rect=True,
#     # augmentations here
# )

from pathlib import Path
from ultralytics import YOLO

DATASET = "dataset/data.yaml"
MODEL = "yolo11n.pt"
OUTPUT = Path(__file__).resolve().parent / "workshop_runs" / "detect"
model = YOLO(MODEL)

model.train(
    data=DATASET,
    epochs=2,
    imgsz=160,
    batch=10,
    project=OUTPUT,
    # device="auto", # for Nvidia GPU users (must have installed pytorch with CUDA)
    device="cpu", # for CPU users
    rect=True,
    # augmentations here
)
