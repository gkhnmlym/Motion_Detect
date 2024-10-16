import cv2
import datetime
import os
import threading
import time
import ctypes

cap = None
out = None
last_motion_time = None
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=25, detectShadows=True)

motion_folder = os.path.join(os.getcwd(), "motion")
if not os.path.exists(motion_folder):
    os.makedirs(motion_folder)

def is_screen_locked():
    user32 = ctypes.windll.User32
    return user32.GetForegroundWindow() == 0

def detect_motion():
    global cap, out, last_motion_time, fgbg

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Unable to open camera!")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Background subtraction
        fgmask = fgbg.apply(frame)
        thresh = cv2.threshold(fgmask, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        motion_area = 0
        for contour in contours:
            if cv2.contourArea(contour) < 3000:  # Ignore small areas to reduce sensitivity
                continue
            (x, y, w, h) = cv2.boundingRect(contour)
            motion_area += w * h
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        frame_area = frame.shape[0] * frame.shape[1]
        if motion_area / frame_area > 0.4:  # Set motion sensitivity to 40%
            motion_detected = True

        if motion_detected and is_screen_locked():
            now = datetime.datetime.now()
            if out is None:
                video_filename = os.path.join(motion_folder, f"motion_{now.strftime('%Y%m%d_%H%M%S')}.avi")
                print(f"Recording video: {video_filename}")
                out = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))
                with open(os.path.join(motion_folder, "motion_log.txt"), "a") as f:
                    f.write(f"Motion detected: {now.strftime('%Y-%m-%d %H:%M:%S')} - {video_filename}\n")
            last_motion_time = time.time()
            out.write(frame)
        else:
            if last_motion_time and (time.time() - last_motion_time) > 3:
                if out:
                    print("Stopping video recorder")
                    out.release()
                    out = None

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    if out:
        out.release()
    if cap:
        cap.release()
    cv2.destroyAllWindows()

def play_video():
    video_path = input("Enter the path of the video to play: ")
    if video_path:
        cap = cv2.VideoCapture(video_path)
        cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
        cv2.moveWindow("Video", 100, 100)  # Set window position (x, y)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Video", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

def delete_video():
    video_path = input("Enter the path of the video to delete: ")
    if video_path:
        os.remove(video_path)
        print("Video successfully deleted!")

def open_video_folder():
    os.startfile(motion_folder)  # Open the motion folder

if __name__ == "__main__":
    # Start motion detection in a separate thread
    threading.Thread(target=detect_motion).start()

    while True:
        print("Options:")
        print("1. Open Video Folder")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("Opening video folder...")
            open_video_folder()
        elif choice == '2':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
