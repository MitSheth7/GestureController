# GestureController
Performing a curl with the left arm -> INITIATE PLAY
Executing a curl with the right arm -> ENGAGE PAUSE
Curling the left leg -> SET VOLUME TO MAXIMUM
Curling the right leg -> SET VOLUME TO MINIMUM
Crossing arms (simultaneous curl with left and right arm) -> TOGGLE MUSIC APP (open/close)
Body movements are monitored by establishing angular points among various nodes. As depicted in the image below, I determined the angle between these points and recognized a “curl” action when they fell below a certain threshold.


# Cases
This application can be beneficial for individuals who have difficulty using their keyboard (the actions would need to be moderated).
An additional use of this project could be for remote operation. For instance, if a person is operating multiple devices and is at a distance from their laptop, basic gestures could prevent the user from having to repeatedly walk over to the laptop.

# Youtube Video
https://youtu.be/FlCVDliozvQ

# Key Insights
This project provided me with a deep understanding of body tracking via mediapipe. I was amazed by the accuracy of each node tracking and the system’s quick response. Prior to this, I was unaware that a MacBook could be manipulated through scripts. This revelation was intriguing, and I thoroughly enjoyed discovering the various functions offered by osascript.

# Key Obstacles 
The most significant hurdle I encountered during this project was determining which movements and at what angles would consistently register with the computer. Given that I was quite far from the computer for the demo, I had to devise clear and repeatable movements that the camera could consistently recognize. I determined the angles through a combination of basic mathematics and a fair amount of trial and error.

# Future Enhancements and Growth
For future versions of this project (particularly if it’s intended for those who can’t use certain laptop features), I would emphasize “simpler” movements, which might necessitate an alternative to mediapipe. I would also concentrate on developing useful functions. In this instance, I used it for music control, but more crucial functions could be incorporated


