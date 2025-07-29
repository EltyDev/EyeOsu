import mediapipe as mp
import cv2 as cv
import time
import threading

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


output_frame = None
frame_lock = threading.Lock()


def process_gesture(result, image, timestamp):
    global output_frame
    hand_landmarks_list = result.hand_landmarks
    annotated_image = image.numpy_view().copy()
    height, width, _ = annotated_image.shape
    for idx in range(len(hand_landmarks_list)):
        hand_landmarks = hand_landmarks_list[idx]
        x_coords = [lm.x for lm in hand_landmarks]
        y_coords = [lm.y for lm in hand_landmarks]
        x = int((max(x_coords) + min(x_coords)) / 2 * width)
        y = int((max(y_coords) + min(y_coords)) / 2 * height)


if __name__ == "__main__":
    base_options = python.BaseOptions(
        model_asset_path="tasks/hand_landmarker.task"
    )
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=2,
        running_mode=vision.RunningMode.LIVE_STREAM,
        result_callback=process_gesture
    )
    recognizer = vision.HandLandmarker.create_from_options(options)
    camera = cv.VideoCapture(0)
    if not camera.isOpened():
        raise RuntimeError("Could not open camera.")

    start_time = time.time()

    while camera.isOpened():
        success, image = camera.read()
        if not success:
            continue
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
        recognizer.detect_async(
            mp_image,
            int((time.time() - start_time) * 1000)
        )
        with frame_lock:
            if output_frame is not None:
                frame_to_show = output_frame.copy()
            else:
                frame_to_show = None
    camera.release()
