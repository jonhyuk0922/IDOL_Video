import cv2
import numpy as np

video_path = 'seventeen_video.mp4'
cap = cv2.VideoCapture(video_path)

output_size = (357, 667) # (width, height)

#initialize writing video
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
out = cv2.VideoWriter('%s_output.mp4' % (video_path.split('.')[0]), fourcc , cap.get(cv2.CAP_PROP_FPS), output_size)

#재생 안될 때
if not cap.isOpened():
    exit()

tracker = cv2.TrackerCSRT_create()


ret, img = cap.read()

cv2.namedWindow('Select Window')
cv2.imshow('Select Window' , img)

# setting ROI(region of interest)
rect = cv2.selectROI('Select Window', img , fromCenter=False, showCrosshair=True)
cv2.destroyWindow('Select Window')

# initializer tracker
tracker.init(img,rect)

while True:
    ret , img = cap.read()

    #비디오 끝났을 때
    if not ret:
        exit()
    
    success, box = tracker.update(img)

    left , top , w , h = [int(v) for v in box]

    center_x = left + w / 2
    center_y = top + h / 2 

    result_top = int(center_y - output_size[1] / 2)
    result_bottom = int(center_y + output_size[1] / 2)
    result_left = int(center_x - output_size[0] / 2)
    result_right= int(center_x + output_size[0] / 2)

    result_img = img[result_top:result_bottom, result_left:result_right].copy()

    out.write(result_img)
    
    cv2.rectangle(img, pt1 =(left, top) , pt2 = (left+w, top +h), color=(255,255,255), thickness=3)

    cv2.imshow('result_img', result_img)
    cv2.imshow('img', img)
    if cv2.waitKey(1) == ord('q'):
        break 