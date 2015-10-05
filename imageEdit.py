# -*- coding: utf-8 -*-
"""
Created on Mon Oct 05 03:47:52 2015

@author: saptaks
"""
import cv2
import numpy as np
from matplotlib import pyplot as plt

class ImageEdit:
    
    def __init__(self, image):       
        self.image = image        

    def resize(self, width, height):  
        return cv2.resize(self.image,(width, height))
        
    def gray(self, w, h):
        img_resize = self.resize(w, h)
        return cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)
        
    def hog(self, bin_n):
        image = self.gray(100, 100)#resize and convert to grayscale
        
        #Finding the Sobel
        gx = cv2.Sobel(image, cv2.CV_32F, 1, 0)
        gy = cv2.Sobel(image, cv2.CV_32F, 0, 1)
        mag, ang = cv2.cartToPolar(gx, gy)
 
        # quantizing binvalues in (0...16)
        bins = np.int32(bin_n*ang/(2*np.pi))
 
        # Divide to 4 sub-squares
        bin_cells = bins[:10,:10], bins[10:,:10], bins[:10,10:], bins[10:,10:]
        mag_cells = mag[:10,:10], mag[10:,:10], mag[:10,10:], mag[10:,10:]
        hists = [np.bincount(b.ravel(), m.ravel(), bin_n) for b, m in zip(bin_cells, mag_cells)]
        hist = np.hstack(hists)
        return hist
    

#Example Use
'''
img = cv2.imread('4.jpg')
im = ImageEdit(img)
hist = im.hog(6)
print hist
img_gray = im.gray(100, 100)
plt.plot(hist)                 #Plots the HOG
plt.xlim([0,256])
plt.show()
cv2.waitKey(0)                 # Waits forever for user to press any key
cv2.destroyAllWindows()
'''