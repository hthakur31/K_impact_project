# traffic_app/video_stream.py

import cv2
from ultralytics import YOLO
from .status import status_data
from .gpio_control import setup_gpio, turn_on_light, cleanup_gpio

model = YOLO("yolov8n.pt")
EMERGENCY_KEYWORDS = ["ambulance", "fire", "police", "fire truck"]

setup_gpio()

def gen_frames():
    cap = cv2.VideoCapture(0)  # webcam or your video source

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            results = model(frame, imgsz=640)[0]

            vehicle_count = 0
            emergency_detected = False

            for box in results.boxes:
                cls = int(box.cls[0])
                class_name = model.names[cls]
                conf = float(box.conf[0])

                if conf > 0.5:
                    xyxy = box.xyxy[0].cpu().numpy().astype(int)
                    label = f"{class_name} {conf:.2f}"
                    cv2.rectangle(frame, tuple(xyxy[:2]), tuple(xyxy[2:]), (0, 255, 0), 2)
                    cv2.putText(frame, label, (xyxy[0], xyxy[1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    if class_name in ["car", "truck", "bus", "motorbike"]:
                        vehicle_count += 1
                    if any(keyword in class_name.lower() for keyword in EMERGENCY_KEYWORDS):
                        emergency_detected = True

            # Update status for dashboard and gpio
            status_data["vehicle_count"] = vehicle_count
            status_data["emergency_detected"] = emergency_detected
            status_data["light_status"] = (
                "green" if emergency_detected or vehicle_count >= 5
                else "yellow" if vehicle_count > 0
                else "red"
            )

            # Traffic light control
            if emergency_detected or vehicle_count >= 5:
                turn_on_light("green")
            elif vehicle_count > 0:
                turn_on_light("yellow")
            else:
                turn_on_light("red")

            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    finally:
        cap.release()
        cleanup_gpio()
