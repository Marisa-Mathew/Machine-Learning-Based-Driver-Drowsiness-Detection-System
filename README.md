# Machine-Learning-Based-Driver-Drowsiness-Detection-System


### Instructions for Machine-Learning-Based Driver Drowsiness Detection System Using Raspberry Pi and OV5467 Camera

This system is designed to detect driver drowsiness using computer vision and machine learning techniques. The key components include a **Raspberry Pi** as the processing unit and an **OV5467 camera module** for real-time frame capture. The analysis is performed using the **Dlib** library for facial landmark detection and **NumPy** for mathematical operations, especially for calculating the **Euclidean distance** between eye landmarks to determine eye aspect ratio (EAR), a metric commonly used to assess drowsiness levels.

---

### 1. **System Requirements**

* Raspberry Pi (preferably 4B with 4GB RAM for performance)
* OV5467 camera module (connected via CSI interface)
* MicroSD card with Raspbian OS installed
* Python 3.x installed
* Required libraries: `dlib`, `numpy`, `opencv-python`, `imutils`

---

### 2. **System Setup**

1. **Camera Setup**: Connect the OV5467 camera to the Raspberry Pi’s CSI port. Enable the camera from the Raspberry Pi configuration settings using `sudo raspi-config`.

2. **Install Dependencies**:

   ```bash
   sudo apt-get update
   sudo apt-get install python3-pip cmake libopenblas-dev liblapack-dev libx11-dev
   pip3 install dlib numpy opencv-python imutils
   ```

3. **Dlib Facial Landmark Model**: Download the pre-trained shape predictor model:

   * `shape_predictor_68_face_landmarks.dat` from [Dlib model zoo](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)

---

### 3. **Working Principle**

The system uses a live video stream from the OV5467 camera. Each frame is processed using Dlib’s face detector and facial landmark predictor. Specifically, landmarks around the eyes (usually points 36 to 41 for the left eye and 42 to 47 for the right eye) are extracted.

The **Eye Aspect Ratio (EAR)** is computed using the Euclidean distances between these landmarks:

$$
EAR = \frac{||p_2 - p_6|| + ||p_3 - p_5||}{2 \times ||p_1 - p_4||}
$$

This ratio decreases when eyes close and remains low if the driver is drowsy. A threshold (commonly around 0.25) is used—if the EAR stays below this for a certain number of consecutive frames (e.g., 20), a drowsiness alert is triggered.

---

### 4. **Code Flow Overview**

* Initialize camera feed.
* Load Dlib face detector and facial landmark predictor.
* For each frame:

  * Convert to grayscale.
  * Detect face.
  * Identify eye landmarks.
  * Calculate EAR using NumPy’s `np.linalg.norm()` for Euclidean distance.
  * If EAR < threshold over continuous frames, trigger a buzzer or alert.

---

### 5. **Applications and Enhancements**

This system is useful in transportation safety to prevent accidents caused by fatigue. It can be enhanced using:

* Audio alerts or vibration motors.
* Integration with vehicle systems to slow down or stop.
* Use of additional sensors like accelerometers for behavior-based fusion.

---

### 6. **Conclusion**

The Raspberry Pi-based drowsiness detection system is a cost-effective and efficient solution for real-time driver monitoring. With lightweight libraries and machine learning techniques like landmark detection and Euclidean distance calculation, it offers practical application in improving road safety.

---

Let me know if you want the actual Python code for this setup too.
