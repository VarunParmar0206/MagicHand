# 🎵 Gesture-Controlled YouTube Music Controller
### Hands-free playback control using Python, MediaPipe, and OpenCV

This project lets you control **YouTube Music on Windows** using simple hand gestures captured through your webcam.  
It uses **MediaPipe** for fast, reliable hand-tracking and **OpenCV** for real-time video processing. Specific gestures are mapped to actions like **Play/Pause**, **Next**, and **Previous**.

The goal is simple: eliminate unnecessary keyboard interruptions and keep the music flowing while you work.

---

## ✨ Features
- Real-time hand gesture recognition  
- Robust hand landmark tracking using MediaPipe Hands  
- Video stream handling with OpenCV  
- System-level control for:
  - **Play / Pause**
  - **Next Track**
  - **Previous Track**
- Works with YouTube Music in browser or desktop app

---

## 🧠 How It Works
1. Webcam feed is captured with OpenCV.  
2. MediaPipe processes each frame to detect hand landmarks.  
3. Gesture logic identifies specific finger patterns or movements.  
4. The script triggers OS-level key presses (e.g., spacebar, arrow keys).  
5. YouTube Music reacts instantly.

---

## 📦 Installation

### 1. Clone the repository
```
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

## 2. Install dependencies
```
pip install opencv-python mediapipe pyautogui
```

## 3. Run the main script(In thedirectory where the Repo is saved):
```
python main
```

