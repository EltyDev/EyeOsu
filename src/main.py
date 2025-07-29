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
    rgb_image = image.numpy_view().copy()
    if result.hand_landmarks:
        for landmarks in result.hand_landmarks:
            for lm in landmarks:
                x = int(lm.x * rgb_image.shape[1])
                y = int(lm.y * rgb_image.shape[0])
                cv.circle(rgb_image, (x, y), 4, (0, 255, 0), -1)
    if result.gestures:
        gesture = result.gestures[0][0]
        gesture_text = f"Gesture: {gesture.category_name}"
        cv.putText(rgb_image, gesture_text, (10, 30),
                   cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv.LINE_AA)
    bgr_image = cv.cvtColor(rgb_image, cv.COLOR_RGB2BGR)
    with frame_lock:
        output_frame = bgr_image


if __name__ == "__main__":
    base_options = python.BaseOptions(
        model_asset_path="tasks/gesture_recognizer.task"
    )
    options = vision.GestureRecognizerOptions(
        base_options=base_options,
        num_hands=1,
        running_mode=vision.RunningMode.LIVE_STREAM,
        result_callback=process_gesture
    )
    recognizer = vision.GestureRecognizer.create_from_options(options)
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
        recognizer.recognize_async(
            mp_image,
            int((time.time() - start_time) * 1000)
        )
        with frame_lock:
            if output_frame is not None:
                frame_to_show = output_frame.copy()
            else:
                frame_to_show = None
        if frame_to_show is not None:
            cv.imshow("Gesture Recognition", frame_to_show)
        if cv.waitKey(5) & 0xFF == 27:
            break
    camera.release()
    cv.destroyAllWindows()
