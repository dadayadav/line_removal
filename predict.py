# import libraries

import cv2
import matplotlib.pyplot as plt
import numpy as np

# import code script

import remove_line_class
from remove_line_class import remove_line

# image plot 
def image_plot(img):
  plt.imshow(img)
  
# Run code 

# run any one method
# method-1  
image = remove_line(r"path/of/img.jpg") 

# method-2
#img = cv2.imread(r"path/to/image.jpg", cv2.IMREAD_COLOR)
#image = remove_line(img)

original_image, final_gray_scale_image, rgb_image, intermidiate_image = image.remove_straight_line()

# output
f, ax = plt.subplots(2,2, figsize= (10,10))
ax[0,0].imshow(original_image)
ax[0,1].imshow(final_gray_scale_image)
ax[1,0].imshow(rgb_image)
ax[1,1].imshow(intermidiate_image)
