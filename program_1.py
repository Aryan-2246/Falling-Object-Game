import cv2
import random
from cvzone.HandTrackingModule import HandDetector

# Setup
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)

# Game variables
object_x = random.randint(100, 1180)
object_y = -50
object_size = 50
score = 0

# Game loop
while True:
    success, img = cap.read()
    if not success:
        continue

    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    # Draw falling object
    object_y += 15  # Fall speed
    cv2.circle(img, (object_x, object_y), object_size, (0, 255, 255), cv2.FILLED)

    # Reset object and update score if caught
    if hands:
        lmList = hands[0]["lmList"]
        ix, iy = lmList[8][:2]

        dist = ((ix - object_x) ** 2 + (iy - object_y) ** 2) ** 0.5
        if dist < object_size:
            score += 1
            object_x = random.randint(100, 1180)
            object_y = -50

    # If object falls past bottom
    if object_y > 720:
        object_x = random.randint(100, 1180)
        object_y = -50

    # Show score
    cv2.putText(img, f"Score: {score}", (50, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 5)

    cv2.imshow("Catch Game", img)
    cv2.waitKey(1)
