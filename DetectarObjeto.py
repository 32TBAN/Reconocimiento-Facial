import cv2
import numpy as np

# Model configuration
config = "./model/yolov3-tiny.cfg"
# Weights
weights = "model/yolov3-tiny.weights"
# Labels
LABELS = open("model/coco-2.names").read().split("\n")

colors = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

net = cv2.dnn.readNetFromDarknet(config, weights)

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Inicia la captura de la cámara (0: cámara por defecto)

while True:
    ret, frame = video.read()
    if not ret:
        break

    # Reducción de la resolución del marco
    frame = cv2.resize(frame, None, fx=0.6, fy=0.6)

    height, width, _ = frame.shape

    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)

    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

    net.setInput(blob)
    outputs = net.forward(ln)

    boxes = []
    confidences = []
    classIDs = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence > 0.5:
                box = detection[:4] * np.array([width, height, width, height])
                (x_center, y_center, w, h) = box.astype("int")
                x = int(x_center - (w / 2))
                y = int(y_center - (h / 2))

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                classIDs.append(classID)

    idx = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.4)

    if len(idx) > 0:
        for i in idx.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            color = colors[classIDs[i]].tolist()
            text = "{}: {:.3f}".format(LABELS[classIDs[i]], confidences[i])
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow("Video", frame)
    key = cv2.waitKey(30) & 0xFF  # Disminución de la tasa de cuadros por segundo (FPS)

    if key == ord("q"):  # Presiona 'q' para salir del bucle
        break

video.release()
cv2.destroyAllWindows()
