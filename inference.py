import cv2
from ultralytics import YOLO

MODEL_FILE = "best.pt"
IMAGE_SIZE = (160, 128)  # width, height
CONFIDENCE = 0.65
DISPLAY_SCALE = 6

def center_crop(frame, size):
    target_width, target_height = size
    height, width = frame.shape[:2]
    target_ratio = target_width / target_height
    frame_ratio = width / height

    if frame_ratio > target_ratio:
        crop_width = int(height * target_ratio)
        left = (width - crop_width) // 2
        return frame[:, left:left + crop_width]

    crop_height = int(width / target_ratio)
    top = (height - crop_height) // 2
    return frame[top:top + crop_height, :]


def main():
    model = YOLO(MODEL_FILE)
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        raise RuntimeError("Could not open the camera")

    while True:
        success, frame = camera.read()
        if not success:
            break

        frame = center_crop(frame, IMAGE_SIZE)
        frame = cv2.resize(frame, IMAGE_SIZE)
        # This is where the inference actually happens
        result = model(
            frame,
            imgsz=IMAGE_SIZE[::-1],
            conf=CONFIDENCE,
            rect=True,
            verbose=False,
        )[0]

        # This is where we draw the bounding boxes and labels on the frame
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            class_id = int(box.cls[0])
            score = float(box.conf[0])
            label = f"{score:.2f}"
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 5, 15)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )
            
        # Resize and display the frame in a window
        display = cv2.resize(
            frame,
            None,
            fx=DISPLAY_SCALE,
            fy=DISPLAY_SCALE,
            interpolation=cv2.INTER_NEAREST,
        )
        cv2.imshow("Live Inference", display)

        if cv2.waitKey(1) & 0xFF in (ord("q"), 27):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
