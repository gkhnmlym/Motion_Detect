import cv2
import face_recognition
import os
import ctypes

# Kendi yüzünüzü kaydedin
KNOWN_FACE_DIR = "known_faces"
if not os.path.exists(KNOWN_FACE_DIR):
    os.makedirs(KNOWN_FACE_DIR)

video_capture = cv2.VideoCapture(0)

# Kendi yüz resminizi burada kaydedin
your_image = face_recognition.load_image_file("path_to_your_image.jpg")
your_face_encoding = face_recognition.face_encodings(your_image)[0]

known_face_encodings = [your_face_encoding]

def lock_screen():
    """Windows ekranı kilitler"""
    ctypes.windll.user32.LockWorkStation()

while True:
    ret, frame = video_capture.read()

    # Görüntüyü küçültmek için (işlemleri hızlandırmak için)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Çerçevedeki tüm yüzleri bul ve karşılaştır
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_found = False
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        if True in matches:
            face_found = True
            break

    if not face_found:
        print("Yabancı bir yüz algılandı! Ekranı kilitliyorum.")
        lock_screen()
        break  # Sonsuz döngüden çık

    # Eğer 'q' tuşuna basılırsa döngüden çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamerayı serbest bırak ve pencereleri kapat
video_capture.release()
cv2.destroyAllWindows()
