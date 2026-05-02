import cv2
import mediapipe as mp
import numpy as np

def calculate_angle(a, b, c):# shoulder , elbow , wrist
    a = np.array(a) # First (Shoulder)
    b = np.array(b) # Mid (Elbow)
    c = np.array(c) # End (Wrist)
    
    # Calculate the radians and convert to degrees
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])#angle at the elbow
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:#if angle greater that 180 ya3ne other side of the elbow
        angle = 360-angle
        
    return angle


# Initialize MediaPipe pose 
mp_pose = mp.solutions.pose#hone here I load the Pose module responsable for detecting the body poses by(mp_pose.Pose())
pose = mp_pose.Pose()#process successive images of the cam 

# Drawing utilities
mp_draw = mp.solutions.drawing_utils# drawing utilities help by drawing the landmark poses and spots on the image , the dots and squeleton


counter = 0 
#stage = None # This will be up or down
# Changed from stage = None
stage_l = None
stage_r = None

# open webcam by defaut 0
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

while True:
    # Read one frame from the webcam
    # the video is a fast sequence of images,
    # the read grabs the next image(frame) from the camera
    # it returns 2 values: ret=boolean(True=Frame was read successfully, False=Somethin went wrong);
    # second: frame stores the image the frame is frame[100][200] = [B, G, R] Height * Width pixels Each pixel has 3 values:,Blue ,Green ,Red (BGR, not RGB)

    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break
        
    # Convert BGR to RGB (MediaPipe needs RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame and detect pose
    results = pose.process(rgb_frame)#detect landmark for the whole body 

# If landmarks are detected, draw them
    if results.pose_landmarks:#contains the the x , y , z coordinates of the 33 body points
        #Draw the skeleton
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Extract specific landmarks
        #I will use the LEFT arm for now (11, 13, 15)
        try:
            landmarks = results.pose_landmarks.landmark#i will access the landmark data as i said for the left arm 
            
            # Get coordinates for Shoulder, Elbow, and Wrist
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]


            # Print the elbow  y coordinate to the console to see it change
            # When you lift left arm
            #print(f"Elbow Y: {elbow[1]}")
            
            #calculate ANGLE
            anglel = calculate_angle(shoulder, elbow, wrist)
            # CURL COUNTER
            if anglel > 160:
                stage_l = "down"
            if anglel < 30 and stage_l == 'down':
                stage_l = "up"
                counter += 1
                print(f"Rep Count left : {counter}")

            shoulderR = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbowR = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            wristR = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            angleR = calculate_angle(shoulderR, elbowR, wristR)

            if angleR > 160:
                stage_r = "down"
            if angleR < 30 and stage_r == 'down':
                stage_r = "up"
                counter += 1
                print(f"Rep Count left : {counter}")
            #DISPLAY ANGLE ON SCREEN 
            # We multiply by image dimensions to put the text near the elbow
            cv2.putText(frame, str(int(anglel)), tuple(np.multiply(elbow, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

            #DISPLAY ANGLE ON SCREEN 
            # We multiply by image dimensions to put the text near the elbow
            cv2.putText(frame, str(int(angleR)), tuple(np.multiply(elbowR, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        except:
            pass
    #DISPLAY COUNTER ON SCREEN
    # Draw a black rectangle at the top left
    cv2.rectangle(frame, (0,0), (225,73), (0,0,0), -1)
    # Put the text for "REPS" and the actual "counter"
    cv2.putText(frame, 'REPS', (15,12), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
    cv2.putText(frame, str(counter), (10,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
    # Put the text for "STAGE"
    #cv2.putText(frame, 'STAGE', (65,12),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
    #cv2.putText(frame, stage, (60,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
    # Show result
    # Show the video frame if detected
    cv2.imshow("Bicep Curl Counter - Webcam", frame)

    # press q to exit waits 1 millisecond
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()