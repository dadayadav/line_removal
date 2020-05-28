import cv2 
import numpy as np
import matplotlib.pyplot as plt
class remove_line:
  def __init__(self, img, image = True, image_path= False):
    if type(img)==type(np.array([0])):
      image= True
      image_path = False
      self.img = img
      self.gray = cv2.cvtColor(self.img,cv2.COLOR_GRAY2RGB)
    else:
      try:
        self.img = cv2.imread(img, cv2.IMREAD_COLOR)
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
      except:
        print(f"No such file exist with name '{img}'")

  def edges(self, img):
    edges = cv2.Canny(img,50,150,apertureSize = 3)
    return edges 

  def houghline(self, edges):
    lines = cv2.HoughLines(edges,1,np.pi/180, 200)
    return lines
  
  def show_wait_destroy(self, img):
    plt.imshow(img)
   
  def detect_horizontal_lines(self, img):
    img = cv2.bitwise_not(img)
    bw = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 15, -2)
    horizontal = np.copy(bw)
    cols = horizontal.shape[1]
    horizontal_size = cols // 30
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
    horizontal = cv2.erode(horizontal, horizontalStructure)
    horizontal = cv2.dilate(horizontal, horizontalStructure)
    self.show_wait_destroy(horizontal)
    return bw, horizontal
  
  def detect_vertical_lines(self,img):
    img = cv2.bitwise_not(img)
    bw = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 15, -2)
    vertical = np.copy(bw)
    rows = vertical.shape[0]
    verticalsize = rows // 30
    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))
    vertical = cv2.erode(vertical, verticalStructure)
    vertical = cv2.dilate(vertical, verticalStructure)
    self.show_wait_destroy(vertical)
    return bw, vertical
  
  def remove_straight_line(self):
    bw, horizontal = self.detect_horizontal_lines(self.gray)
    bw, vertical = self.detect_vertical_lines(self.gray)
    img = np.copy(horizontal)
    vet = np.copy(vertical)
    img = cv2.bitwise_not(img)
    vet = cv2.bitwise_not(vet)
    edge = self.edges(img)
    edge_vet = self.edges(vet)
    lines = self.houghline(edge)
    try:
      print("Horizontal line Detection start.......")
      for i in lines:
        for r,theta in i: 
            a = np.cos(theta) 
            b = np.sin(theta) 
            x0 = a*r 
            y0 = b*r 
            x1 = int(x0 + 1000*(-b)) 
            y1 = int(y0 + 1000*(a))  
            x2 = int(x0 - 1000*(-b)) 
            y2 = int(y0 - 1000*(a)) 
            cv2.line(img,(x1,y1), (x2,y2), (0,0,0))
      print("Horizontal Line Removed")
    except:
      print("No horizontal line detected")
      
    lines = self.houghline(edge_vet)
    try:
      print("Vertical line detection start.......")
      for i in lines:
        for r,theta in i: 
            a = np.cos(theta) 
            b = np.sin(theta) 
            x0 = a*r 
            y0 = b*r 
            x1 = int(x0 + 1000*(-b)) 
            y1 = int(y0 + 1000*(a))  
            x2 = int(x0 - 1000*(-b)) 
            y2 = int(y0 - 1000*(a)) 
            cv2.line(vet,(x1,y1), (x2,y2), (0,0,0))
      print("Vertical Line Removed")
    except:
      print("No vertical line detected")
    vet = cv2.bitwise_not(vet)
    img = cv2.bitwise_not(img)
    a = np.copy(bw)
    final = np.subtract(a, img)
    final = np.subtract(final,vet)
    final = cv2.bitwise_not(final)
    a = np.copy(self.gray)
    a = cv2.bitwise_and(a,final)
    backtorgb = cv2.cvtColor(a,cv2.COLOR_GRAY2RGB)
    self.show_wait_destroy(backtorgb)
    return self.img, final, backtorgb, bw
