
"""
Created on Wed Jun  9 15:38:35 2021

@author: Alysson
"""

import cv2
import numpy as np
import glob
import os

# This method does not have a use. Required only for Trackbar generation.
def nothing(x):
    pass

class Screen:
    '''Class responsible for the graphic interface and user input'''
    
    def __init__(self, path):
        
        self.process = Processing()
        
        # Get images from folder and place in an array. 
        # Only the first one is used for interface phase.
        self.image_list, self.filename_list = self.process.get_images(path)
        self.img = self.image_list[0]
               
        cv2.namedWindow('Trackbars')
        cv2.createTrackbar("Lower H", "Trackbars", 0, 179, nothing)
        cv2.createTrackbar("Upper H", "Trackbars", 179, 179, nothing)
        cv2.createTrackbar("Lower S", "Trackbars", 0, 255, nothing)
        cv2.createTrackbar("Upper S", "Trackbars", 255, 255, nothing)
        cv2.createTrackbar("Lower V", "Trackbars", 0, 255, nothing)
        cv2.createTrackbar("Upper V", "Trackbars", 255, 255, nothing)
               
    def show(self):
        '''Initialize all windows'''
        print('Waiting user input. Press ESC to confirm HSV range.')
         
        while True:
         
            l_h = cv2.getTrackbarPos("Lower H", "Trackbars")
            l_s = cv2.getTrackbarPos("Lower S", "Trackbars")
            l_v = cv2.getTrackbarPos("Lower V", "Trackbars")
            u_h = cv2.getTrackbarPos("Upper H", "Trackbars")
            u_s = cv2.getTrackbarPos("Upper S", "Trackbars")
            u_v = cv2.getTrackbarPos("Upper V", "Trackbars")
            
            self.process.update(l_h, l_s, l_v, u_h, u_s, u_v)
            mask, rmv_bg = self.process.masking(self.img, True)        

            cv2.imshow('mask', mask)
            cv2.imshow('input', rmv_bg)
            
            key = cv2.waitKey(1)         
            if key == 27:
                cv2.destroyAllWindows()
                break
            
        self.process.save(self.image_list, self.filename_list)
            
            
       
class Processing:
    '''Class responsible for image processing steps'''
    
    def __init__(self):
        self.l_h = 0
        self.l_s = 0
        self.l_v = 0
        self.u_h = 179
        self.u_s = 255
        self.u_v = 255
        
    def get_images(self, path):
        '''Reads the folder containing the images. Returns a list with the image matrixes and another list with each image filename'''
        print('Importing images from folder...')
        
        img_list = []
        img_name = []
        
        for file in glob.glob(path):
            image = cv2.imread(file)
            name = os.path.basename(file)
            
            img_list.append(image) #list which contains the images
            img_name.append(name) #list which contais each image filename
            
        
        
        return img_list, img_name
        
        
    def update(self, l_h, l_s, l_v, u_h, u_s, u_v):
        '''Updates the values from the trackbar while user is adjusting'''
        
        self.l_h = l_h
        self.l_s = l_s
        self.l_v = l_v
        self.u_h = u_h
        self.u_s = u_s
        self.u_v = u_v
        
    def masking(self, img, screen_flag):
        '''Creates the mask. Returns the masked RGB image and/or the binary mask'''
        
        lhsv = np.array([self.l_h , self.l_s, self.l_v])
        uhsv = np.array([self.u_h, self.u_s, self.u_v])
        
        # image need to be resized to fit the screen.
        img_downscale = cv2.resize(img, (900, 600))
        hsv = cv2.cvtColor(img_downscale, cv2.COLOR_BGR2HSV)
         
        mask = cv2.inRange(hsv, lhsv, uhsv)
        
        # noise filter to remove isolated pixels
        kernel = np.ones((3,3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # stack mask over imput image only for interface stage
        if (screen_flag == True):
            rmv_bg = cv2.bitwise_and(img_downscale, img_downscale, mask = mask)
            return mask, rmv_bg
        
        else:
            return mask
    
    def save(self, image_list, filename_list):
        '''Iterates through each image from the list for masking and saves the resultant masks in a folder. 
        The name of the mask is designed to be compatible with Agisoft Metashape mask importing requirements'''
        print('Processing masks...')
        
        for i in range(len(image_list)):
            filename = filename_list[i]
            filename = filename[:-4]
            mask = self.masking(image_list[i], False)
             
            mask_upscale = cv2.resize(mask, (6000, 4000))
            
            cv2.imwrite('images_mask/' + filename + '_mask.jpg', mask_upscale)
        
        print('Masks saved!' )
    
           
path = 'images/*.jpg' # folder path that contains the images. The * is required by the glob.glob() method   
tela = Screen(path)
tela.show()


    