import cv2
import numpy as np
import utilities
import bfs
from time import sleep

image =""
#cam = cv2.VideoCapture(0)

def robotPosition():
    global image
    # Load image
    #ret, frame = cam.read()

    image = cv2.imread("/Users/rugvedchavan/Desktop/PathImg/grid.png")
    image = cv2.resize(image, (1280 , 720))
    cv2.imshow("Image", image)

    font = cv2.FONT_HERSHEY_SIMPLEX

    # Convert to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("gray", gray)

    # bulr the image kernel size 9*9
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    #cv2.imshow("blur", blur)

    # Thrushold
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 5, 2)
    #cv2.imshow("thresh", thresh)

    # Get Contours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Get the outer box
    max_area = 0
    c = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 1000:
            if area > max_area:
                max_area = area
                best_cnt = i
                image = cv2.drawContours(image, contours, c, (0, 255, 0), 3)
        c += 1

    # mask white BG
    mask = np.zeros((gray.shape), np.uint8)
    cv2.drawContours(mask, [best_cnt], 0, 255, -1)
    cv2.drawContours(mask, [best_cnt], 0, 0, 2)
    #cv2.imshow("mask", mask)

    # copy mask on outer box
    out = np.zeros_like(gray)
    out[mask == 255] = gray[mask == 255]
    #cv2.imshow("New image", out)

    # blur 9*9 kernal filter
    blur = cv2.GaussianBlur(out, (9, 9), 0)
    #cv2.imshow("blur1", blur)

    # threshhold
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
    #cv2.imshow("thresh1", thresh)

    # get contours 2
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # sort the contours "top-to-bottom"
    contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * image.shape[1])


    # get inside every contours
    global top,bottom,value
    count = 0
    m = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 1000/ 2 and area < 10000:
            approx = cv2.approxPolyDP(i, 0.08 * cv2.arcLength(i, True), True)
            x = approx.ravel()[0]
            y = approx.ravel()[1]
            # CHEAK FOR RECTANGLE
            if len(approx) == 4:
                m = m+1

                # compute the center of the contour
                M = cv2.moments(i)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                # DRAW AND NUMBER Text BOX
                cv2.drawContours(image, contours, count, (0, 255, 0), 3)
                cv2.putText(image, str(m), (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

                # print(i) # cordinates of contours detected
                # j.append(i)

                # ALGO
                # mask real image with ideal image
                RealImage = cv2.imread("/Users/rugvedchavan/Desktop/PathImg/grid4.png")
                #RealImage = frame   #For Camera
                RealImage = cv2.resize(RealImage, (1280 , 720))
                cv2.imshow("RealImage", RealImage)

                # mask contour on img
                best_cnt = i
                mask = np.zeros((gray.shape), np.uint8)
                cv2.drawContours(mask, [best_cnt], 0, 255, -1)
                cv2.drawContours(mask, [best_cnt], 0, 0, 2)
                #cv2.imshow("test3", mask)
                mask = cv2.resize(mask, (1280 , 720))

                # copy mask on outer box
                out = np.zeros_like(RealImage)
                out[mask == 255] = RealImage[mask == 255]
                cv2.imshow("test4", out)
                out1 = out

                ##############################

                # mask contour on img
                best_cnt = i
                mask = np.zeros((gray.shape), np.uint8)
                cv2.drawContours(mask, [best_cnt], 0, 255, -1)
                cv2.drawContours(mask, [best_cnt], 0, 0, 2)
                #cv2.imshow("test1", mask)

                # copy mask on outer box
                out = np.zeros_like(image)
                out[mask == 255] = image[mask == 255]
                #cv2.imshow("test2", out)

                # convert to BGR
                hsv = cv2.cvtColor(out1, cv2.COLOR_BGR2HSV)

                # check red color for top array
                a = utilities.detectRed(mask, hsv)
                if(m <= 28):
                    top.append(a)
                elif(m > 28):
                    bottom.append(a)

                #cv2.waitKey(0)
        count += 1
while(True):
    value = 999
    top = []
    bottom = []
    robotPosition()
    # print final image
    cv2.resize(image, (320, 480))  
    cv2.imshow("Final Image", image)

    path=[]
    # Top array
    R = 7 #7
    C = 4 #4
    print("top: " , top)
    entries = list(map(str, top))
    try: 
        top = np.array(entries).reshape(R, C)
        top[6][3] = "X"
        
    except:
        top[6][3] = "X" # 6,3
        print(top)
        print(" array problem line 142")
        
    try:
        path.append(bfs.main1(top))  # BSF
    except Exception as e:
        print(e)
        print("problem 1 !!")

    # Bottom array
    if ('O' in bottom): # O
        R=2
        C=16
        entries = list(map(str, bottom))
        bottom = np.array(entries).reshape(R, C)
        bottom[0][15] = "X"
        bottom[0][13] = " "
        print(bottom)

        try:
            path.append(bfs.main1(bottom)) # BSF
        except Exception as e:
            print(e)
            print("problem 2 !!")

    # Print total path
    path = "D".join(path)
    print("total path = " + str(path))

    # Send to Robot 1
    utilities.send(path[0],"192.168.43.195")
    # Send to Robot 2
    utilities.send(path,"192.168.43.195")
    # Send to Robot 3
    utilities.send(path,"192.168.43.195")
    # Send to Robot 4
    utilities.send(path,"192.168.43.195")

    #sleep(1)
    cv2.waitKey(0)
    
cv2.destroyAllWindows()


