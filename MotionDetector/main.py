import cv2
import datetime
import os
import threading
import time
import ctypes
import tkinter as tk
from tkinter import ttk, messagebox

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

def start_camera():
    global cap
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Hata", "Kamera açılamadı!")
        return

    threading.Thread(target=detect_motion).start()

def detect_motion():
    global cap, out, last_motion_time, fgbg

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

def open_video_folder():
    os.startfile(motion_folder)  # Open the motion folder

def on_closing(root):
    # Pencere kapatıldığında tüm işlemleri sonlandır
    root.destroy()
    os._exit(0)

def create_gui():
    root = tk.Tk()
    root.title("Kamera İzni Uygulaması")

    # Pencere boyutunu sabitleme
    root.geometry("400x250")
    root.resizable(False, False)  # Pencere yeniden boyutlandırılamaz

    # Koyu tema için arka plan ve yazı renkleri
    root.configure(bg='#2c2c2c')  # Koyu gri arka plan

    # Stiller
    style = ttk.Style()
    style.theme_use('clam')

    style.configure("TButton", font=("Helvetica", 12), padding=10, background='#444444', foreground='#ffffff', borderwidth=0)
    style.configure("TLabel", font=("Helvetica", 14), padding=10, background='#2c2c2c', foreground='#ffffff')

    style.map("TButton",
              background=[('active', '#555555')],
              relief=[('pressed', 'flat'), ('!pressed', 'ridge')],
              bordercolor=[('!pressed', '#2c2c2c')],
              focuscolor=[('!focus', '#2c2c2c')])

    # Başlık
    title_label = ttk.Label(root, text="Kamera Erişim İzni", anchor="center")
    title_label.pack(pady=20)

    # İzin Ver Butonu
    def on_request_permission():
        start_camera()
        messagebox.showinfo("Başarılı", "Kamera izni verildi ve kamera başlatıldı.")

    permission_button = ttk.Button(root, text="İzin Ver", command=on_request_permission)
    permission_button.pack(pady=10)

    # Kayıt Dosya Konumunu Aç Butonu
    def on_open_folder():
        open_video_folder()

    open_folder_button = ttk.Button(root, text="Kayıt Dosya Konumunu Aç", command=on_open_folder)
    open_folder_button.pack(pady=10)

    # Pencereyi kapatırken programı sonlandırma
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

    root.mainloop()

if __name__ == "__main__":
    create_gui()
