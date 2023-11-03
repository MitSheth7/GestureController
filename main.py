import cv2
import mediapipe as mp
import numpy as np
import osascript

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

user_input = input("Press [1] to start the program or Press [2] to view instructions: ")

if user_input == '2':
    print('Instructions:')

if user_input == '1':
    print("press [q] to quit at any time.")


def calculate_angle(point1, point2, point3):
    point1 = np.array(point1)
    point2 = np.array(point2)
    point3 = np.array(point3)

    radians = np.arctan2(point3[1] - point2[1], point3[0] - point2[0]) - np.arctan2(point1[1] - point2[1],
                                                                                    point1[0] - point2[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


cap = cv2.VideoCapture(0)

counter = 0
stage = None
command = ''

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates of different body parts
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

            nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x,
                    landmarks[mp_pose.PoseLandmark.NOSE.value].y]

            # Calculate angles
            left_bicep_curl_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
            right_bicep_curl_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
            left_leg_curl_angle = calculate_angle(left_hip, left_knee, left_ankle)
            right_leg_curl_angle = calculate_angle(right_hip, right_knee, right_ankle)

            # PLAY Command Logic
            if left_bicep_curl_angle > 160:
                stage = "downArmLeft"
            if left_bicep_curl_angle < 30:
                command = 'PLAY'
                osascript.osascript('tell application "music" to play')

            # PAUSE Command Logic
            if right_bicep_curl_angle > 160:
                stage = "downArmRight"
            if right_bicep_curl_angle < 30:
                command = 'PAUSE'
                osascript.osascript('tell application "music" to pause')

            # VOLUME 100 Command Logic
            if left_leg_curl_angle > 160:
                stage = "downLegLeft"
            if left_leg_curl_angle < 100:
                command = 'VOLUME 100'
                osascript.osascript('set volume output volume 100')

            # VOLUME 0 Command Logic
            if right_leg_curl_angle > 160:
                stage = "downLegRight"
            if right_leg_curl_angle < 100:
                command = 'VOLUME 0'
                osascript.osascript('set volume output volume 0')

            # OPEN MUSIC Command Logic
            if right_bicep_curl_angle < 90 and left_bicep_curl_angle < 90:
                if counter % 2 == 0:
                    command = 'OPEN MUSIC'
                    osascript.osascript('tell application "music" to activate')
                else:
                    command = 'CLOSE MUSIC'
                    osascript.osascript('quit app "music.app"')
                counter += 1

        except:
            pass

        # Show Command
        cv2.putText(image, 'Command',
                    (65, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(image, command,
                    (60, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2, cv2.LINE_AA)

        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                  )

        cv2.imshow('Output Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
