import cv2
import numpy as np
import socket
import time

def detectRed(img,hsv):
    # define range wanted color in HSV

    lower_val = np.array([0, 50, 50])
    upper_val = np.array([10, 255, 255])

    # Threshold the HSV image - any green color will show up as white
    mask = cv2.inRange(hsv, lower_val, upper_val)

    # if there are any white pixels on mask, sum will be > 0
    hasGreen = np.sum(mask)
    if hasGreen > 0:
        print('red detected!')
        return "O"
    else:
        k = detectBlue(img, hsv)
        return k

    # show image
    # apply mask to image
    res = cv2.bitwise_and(img,img,mask=mask)
    fin = np.hstack((img,res))
    # display image
    cv2.imshow("Res", fin)
    cv2.imshow("Mask", mask)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

def detectRed1(img,hsv):
    # define range wanted color in HSV

    lower_val = np.array([0, 50, 50])
    upper_val = np.array([10, 255, 255])

    # Threshold the HSV image - any green color will show up as white
    mask = cv2.inRange(hsv, lower_val, upper_val)

    # if there are any white pixels on mask, sum will be > 0
    hasGreen = np.sum(mask)
    if hasGreen > 0:
        print('red detected!')
        return "X"
    else:
        print('Not detected')
        return " "

    # show image
    # apply mask to image
    res = cv2.bitwise_and(img,img,mask=mask)
    fin = np.hstack((img,res))
    # display image
    cv2.imshow("Res", fin)
    cv2.imshow("Mask", mask)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

def detectBlue(img,hsv):
    # define range wanted color in HSV

    sensitivity = 15
    lower_val = np.array([110, 50, 50])
    upper_val = np.array([130, 255, 255])

    # Threshold the HSV image - any green color will show up as white
    mask = cv2.inRange(hsv, lower_val, upper_val)

    # if there are any white pixels on mask, sum will be > 0
    hasGreen = np.sum(mask)
    if hasGreen > 0:
        print('Blue detected!')
        return "#"
    else:
        print('Blue Not detected')
        return " "

    # show image
    # apply mask to image
    res = cv2.bitwise_and(img,img,mask=mask)
    fin = np.hstack((img,res))
    # display image
    cv2.imshow("Res", fin)
    cv2.imshow("Mask", mask)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

#detectRed(img,hsv)
#detectWhite(img,hsv)
    
def send(path,ip):
    array = list(path)
    print(array)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_hostname = socket.gethostname()
    local_fqdn = socket.getfqdn()
 
    #ip_address = socket.gethostbyname(local_hostname)
    port = 55470
    #ip_address = socket.gethostbyname('127.0.1.1')
    ip_address = socket.gethostbyname(ip)
    server_address = (ip_address, port)
    print(server_address)
    sock.connect(server_address)
 
    #print (f"Connecting to {local_hostname} ({local_fqdn}) with {ip_address}")
    print ("Connected to server-side. ")
 
    time.sleep(2)
 
    new_data1 = str(path).encode("utf-8")
    sock.sendall(new_data1)

    time.sleep(2)

    #sock.close()

#send("hello123")  
