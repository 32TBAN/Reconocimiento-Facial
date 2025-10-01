import cv2
import os
from ultralytics import YOLO

def cap_object(video_path=None):
    model = YOLO("yolov8n.pt")

    if video_path is not None:
        if os.path.isfile(video_path) and video_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            frame = cv2.imread(video_path)
            frame = cv2.resize(frame, None, fx=1.5, fy=1.5)

            results = model(frame)

            annotated = results[0].plot()

            cv2.imshow("Image", annotated)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return
        else:
            video = cv2.VideoCapture(video_path)
    else:
        video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
        ret, frame = video.read()
        if not ret:
            break

        results = model(frame, verbose=False)

        annotated = results[0].plot()

        cv2.imshow("Video", annotated)

        key = cv2.waitKey(30) & 0xFF
        if key == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()


# Ejemplo
# cap_object("./Img/city.jpg")  # Imagen
# cap_object("./Videos/demo.mp4")  # Video
# cap_object()  # Cámara en vivo
