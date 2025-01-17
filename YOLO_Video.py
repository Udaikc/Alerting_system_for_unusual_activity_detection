from ultralytics import YOLO
import cv2
import math
from dotenv import load_dotenv
import os

load_dotenv()

# Twilio credentials
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_number = os.getenv("TWILIO_FROM_NUMBER")
to_number = os.getenv("TWILIO_TO_NUMBER")
bin_url = os.getenv("TWILIO_BIN_URL")

def make_call():
    from twilio.rest import Client

    client = Client(account_sid, auth_token)
    call = client.calls.create(
        to=to_number,
        from_=from_number,
        url=bin_url
    )
    print(f"Call initiated, SID: {call.sid}")

def video_detection(path_x):
    video_capture = path_x
    # Create a Webcam Object
    cap = cv2.VideoCapture(video_capture)
    model = YOLO("YOLO-Weights/best.pt")
    classNames = ['Balaclava', 'fire', 'knife', 'pistol', 'smoke']
    colors = {
        'Balaclava': (255, 0, 0),
        'fire': (0, 255, 255),
        'knife': (0, 0, 255),
        'pistol': (0, 255, 0),
        'smoke': (128, 0, 128)
    }

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to read frame from video capture.")
            break  # Exit the loop if frames cannot be read

        results = model(img, stream=True)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                conf = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])
                class_name = classNames[cls]
                label = f'{class_name} {conf}'
                t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                c2 = x1 + t_size[0], y1 - t_size[1] - 3

                color = colors.get(class_name, (85, 45, 255))

                if conf > 0.5:
                    cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
                    cv2.rectangle(img, (x1, y1), c2, color, -1, cv2.LINE_AA)  # filled
                    cv2.putText(img, label, (x1, y1 - 2), 0, 1, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)

                    # Trigger call for specific labels
                    if class_name in ['fire', 'knife', 'pistol']:
                        make_call()

        # Check if img is valid before yielding
        if img is not None and not img.empty():
            yield img
        else:
            print("Detected empty image.")

cv2.destroyAllWindows()