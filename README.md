# Motion_Detect

🎯 Project Purpose
This project is designed to enhance computer security by detecting motion when the system is locked and capturing potential threats through image recording. It operates silently in the background and triggers when unauthorized movement is detected, ensuring that suspicious activities are recorded even when the computer is locked.

🛠️ Technologies and Libraries Used
Python 3.8: The core programming language used for this project.
cv2 (OpenCV): Handles motion detection and image capture from the webcam.
datetime: Adds timestamps to captured images for accurate logging of events.
os: Manages file operations, such as saving captured images to a directory.
threading: Implements multi-threading to ensure smooth and responsive background operation.
time: Controls timing delays for image capture and detection processes.
ctypes: Interacts with system-level APIs to detect if the computer is locked.
tkinter: Optionally used to create a graphical user interface for user interaction.
🚀 Features
Motion Detection: The system can detect motion when the computer is locked, helping monitor and secure the system.
Automatic Image Capture: Automatically captures images upon detecting movement.
Multi-threading Support: Ensures motion detection runs seamlessly in the background without affecting system performance.
Timestamped Image Files: Images are saved with timestamped filenames for easier event tracking.
User-Friendly Interface (Optional): Provides a simple GUI to start and stop the monitoring process.
⚙️ Installation Instructions
Clone the Repository:

git clone https://github.com/yourusername/computer-lock-motion-detection.git
cd computer-lock-motion-detection
Install Required Libraries: Install the necessary Python libraries with pip:

🧑‍💻 Usage
Once the program is running:

The system will monitor for any movements while your computer is locked.
Upon detecting motion, it will automatically capture images and store them in the designated folder.
If enabled, the GUI allows you to control the monitoring settings.
👨‍💻 Contributing
Feel free to contribute to this project by submitting issues or pull requests. All contributions are welcome.

📜 License
This project is licensed under the MIT License.
