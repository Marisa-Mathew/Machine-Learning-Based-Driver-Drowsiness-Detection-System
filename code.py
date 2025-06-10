GPIO.output(LED_PIN, GPIO.HIGH)
    GPIO.output(BUZZER_PIN, GPIO.HIGH)

# Function to deactivate LED and buzzer
def deactivate_alert():
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.output(BUZZER_PIN, GPIO.LOW)

# Main function for real-time monitoring
def monitor_driver():
    # Initialize the Picamera2 instance
    cam = Picamera2()
    preview_config = cam.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)})
    cam.configure(preview_config)
    cam.start()

    drowsy_start_time = None  # To track when the drowsy state starts

    try:
        while True:
            # Capture a frame
            frame = cam.capture_array()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)

            if len(faces) == 0:
                cv2.putText(frame, 'No Face Detected', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                activate_alert()
                drowsy_start_time = None  # Reset drowsy timer
            else:
                # Deactivate alert if a face is detected
                deactivate_alert()

                # Find the closest face based on the bounding box area
                closest_face = max(faces, key=lambda face: face.width() * face.height())
                landmarks = predictor(gray, closest_face)

                # Extract eye and mouth landmarks
                left_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)])
                right_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)])
                mouth = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(48, 68)])

                # Calculate EAR and MAR
                ear_left = eye_aspect_ratio(left_eye)
                ear_right = eye_aspect_ratio(right_eye)
                mar = mouth_aspect_ratio(mouth)

                # Determine driver state based on EAR and MAR
                if ear_left < EYE_AR_THRESH and ear_right < EYE_AR_THRESH:
                    state = "Drowsy"
                    color = (0, 0, 255)  # Red color for drowsy
                    if drowsy_start_time is None:
                        drowsy_start_time = time.time()  # Start the timer
                    elif time.time() - drowsy_start_time > DROWSY_DURATION:
                        activate_alert()  # Activate alert only if drowsy for more than the threshold
                else:
                    state = "Active"
                    color = (0, 255, 0)  # Green color for active
                    drowsy_start_time = None  # Reset drowsy timer
                    deactivate_alert()

                # Draw landmarks and state on the frame
                cv2.polylines(frame, [left_eye], isClosed=True, color=color, thickness=2)
                cv2.polylines(frame, [right_eye], isClosed=True, color=color, thickness=2)
                cv2.polylines(frame, [mouth], isClosed=True, color=color, thickness=2)
                
                # Display the state on the frame
                cv2.putText(frame, f'State: {state}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            cv2.imshow('Driver Fatigue Monitoring', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\nExiting program.")

    finally:
        cam.stop()
        deactivate_alert()
        GPIO.cleanup()
        cv2.destroyAllWindows()

if name == "main":
    monitor_driver()