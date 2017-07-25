import cv2
from util import parse_str as pstr
img = cv2.imread(r"C:\Users\haozhang\Desktop\b0cc9407b98ed5094477725b3025d9930a92573c.jpg")

with open(r"C:\Users\haozhang\Desktop\b0cc9407b98ed5094477725b3025d9930a92573c.txt") as f:
    lines = f.readlines()
p = pstr(lines)
for i in p:
    cv2.rectangle(img, (int(i[0]), int(i[1])),(int(i[2]),int(i[3])),(0,255,0),3)
print(p)
cv2.imshow("t", img)
cv2.waitKey(0)
