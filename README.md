# 🎵MagicHand
This project turns your webcam into a hands-free control system for YouTube Music on Windows. It uses MediaPipe for fast, reliable hand-tracking and OpenCV for real-time video processing. Specific hand gestures trigger playback actions like Play/Pause, Next Track, and Previous Track.

This project lets you control YouTube Music playback on Windows using simple hand gestures captured through your webcam. It uses MediaPipe for hand-tracking and OpenCV for real-time video processing, mapping specific gestures to actions like Play/Pause, Next, and Previous.

The goal is simple: cut out unnecessary keyboard interruptions while keeping the music flowing.

✨ Features
1)Real-time hand gesture detection
2)Accurate hand landmark tracking via MediaPipe
3)Smooth video feed processing with OpenCV
4)System-level control for:
  Play / Pause
  Next Track
  Previous Track
5)Works with YouTube Music (Web or Desktop App)

🧠 How It Works
1)Your webcam feed is captured using OpenCV.
2)MediaPipe identifies hand landmarks in each frame.
3)Your gesture logic interprets finger patterns.
4)The script triggers OS-level key presses (e.g., space, arrow keys).
5)YouTube Music responds instantly.

