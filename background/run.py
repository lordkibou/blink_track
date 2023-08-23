#Improve:
# When staring down, the ratio decreases and it counts blinks
# In order to avoid this problem, we need to have a previous difference with the ratio
# In other words, to count a blink we need to have a previous state when we were not constantly blinking, eyes closed
# or staring to a point which makes our eyes look smaller and count a blink


#Imports from libraries
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot

# Open a video capture stream (0 is usually the default webcam)
cap = cv2.VideoCapture(0)

#Face Detector Initiated
detector = FaceMeshDetector(maxFaces = 1)

#Plot for Ratio Indicator and Graph
plotY = LivePlot(640,480,[20,50], invert = True)

#List that will save ratios, max length 3
ratioList = []

#Counter for the blink
blinkCounter = 0

#Counter for the frames Max will be 10
frameCounter = 0

#ids points that surround the eye
idList = [22,23,24,26,110,157,158,159,160,161,130,243]

while True:
    #Reset Frames when Meets the max frame count
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Read a frame from the video stream
    ret, frame = cap.read()
    
    #Resize the video capture stream
    img = cv2.resize(frame,(640,360))
    
    #Find face
    img, faces = detector.findFaceMesh(frame,draw = False)
    
    #Draw filled purple circles around the detected eye
    if faces:
        face = faces[0]
        for id in idList:
            cv2.circle(img, face[id],3,(255,0,255),cv2.FILLED)
        
        #-------------------------------------------------------
        #Ratio Horizontal and Vertical Line inside the Eye doing a normalization of 3 values
        leftUp = face[159]
        leftLeft = face[130]
        leftDown = face[23]
        leftRight = face[243]
        verticalLength,_ = detector.findDistance(leftUp,leftDown)
        horizontalLength,_ = detector.findDistance(leftLeft,leftRight)
        cv2.line(img, leftUp, leftDown,(0,200,0),2)
        cv2.line(img, leftLeft,leftRight,(0,200,0),2)
        
        ratio = int((verticalLength/horizontalLength)*100)
        
        ratioList.append(ratio)
        if len(ratioList)>3:
            ratioList.pop(0)
        
        ratioAvg = sum(ratioList)/len(ratioList)
        #------------------------------------------------------
        
        #------------------------------------------------------
        # Count blink ignoring the 10 next frames, in order not to have colliding frames and exceed the counter
        if ratioAvg < 34 and frameCounter == 0:
            blinkCounter += 1
            frameCounter = 1
        elif frameCounter < 10 and frameCounter >0:
            frameCounter +=1
        elif frameCounter == 10:
            frameCounter = 0
        #------------------------------------------------------
        
        #Text with Blink Counter
        cvzone.putTextRect(img,f'Blink Count: {blinkCounter}',(50,100))
        
        #Plot with graph ratio
        imgPlot = plotY.update(ratioAvg)
        
    # Display the resulting windows video and plot
        videoPlot = cvzone.stackImages([img, imgPlot], 2, 1)
    cv2.imshow("Live Video", videoPlot)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release the capture stream and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()