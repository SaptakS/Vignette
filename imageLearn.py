# -*- coding: utf-8 -*-
"""
Created on Mon Oct 05 05:18:53 2015

@author: saptaks
"""
import cv2
import glob
import pickle
from imageEdit import ImageEdit as ie

'''
    Storing Links for Each Image
'''
artist_folders = glob.glob('imageDB/*')
artist_img_list = []
for folder in artist_folders:
    folder += '\*.jpg'
    image_list = glob.glob(folder)
    artist_img_list.append(image_list)
    
'''
    Reading Images
    Creating their HOG using imageEdit
    Storing in a 2d Array
'''    
artist_img_hog = []
for img_list in artist_img_list:
    artist_hog = []
    for img in img_list:
        image = cv2.imread(img)
        if(image == None):
            continue            
        hog = ie(image).hog(6)
        #print image
        artist_hog.append(hog)
        
    artist_img_hog.append(artist_hog)

'''Creating a Pickle for Storing HOG'''        
hog_pickle = open("pickled_hog/hog.pickle", "wb")
pickle.dump(artist_img_hog, hog_pickle)
hog_pickle.close()