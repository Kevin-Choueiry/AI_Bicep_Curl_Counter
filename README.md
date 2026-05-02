# AI_Bicep_Curl_Counter
An AI powered bicep curl counter that uses computer vision and pose estimation to track arm joints and calculate angles in real time.The system analyzes body movement through a webcam  to automatically detect and count correct repetitions.
# AI Bicep Curl Counter

A real-time computer vision application built with **Python**, **OpenCV**, and **MediaPipe** that tracks bicep curl repetitions for both arms simultaneously. This tool uses pose estimation to calculate elbow angles and count reps based on the full range of motion.

## 🚀 Features
*   **Dual Arm Tracking:** Independently monitors left and right arm movements.
*   **Real-time Angle Calculation:** Uses trigonometric functions (arctan2) to determine the exact joint angle between the shoulder, elbow, and wrist.
*   **Automatic Rep Counting:** Detects "Up" and "Down" stages based on configurable angle thresholds (e.g., >160° for extension, <30° for contraction).
*   **Visual Feedback:** Overlays a live rep counter and dynamic joint angles directly onto the webcam feed.

## 🛠️ Tech Stack
*   **Language:** Python
*   **Computer Vision:** [OpenCV](https://opencv.org/)
*   **Pose Estimation:** [MediaPipe Pose](https://google.github.io/mediapipe/solutions/pose.html)
*   **Math:** NumPy

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Kevin-Choueiry/AI_Bicep_Curl_Counter.git](https://github.com/Kevin-Choueiry/AI_Bicep_Curl_Counter.git)
   cd AI_Bicep_Curl_Counter
