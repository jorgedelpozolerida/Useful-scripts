# from PIL import Image
import numpy as np
import glob
import os
import cv2
# from pathlib import Path, PureWindowsPath


def extractImages(pathIn, pathOut, n_frames, sel_type='n_frames'):
    '''
    pathIn: path of image to process
    pathOut: path where extracted images should be saved
    every_what: number of miliseconds we take a snap
    '''
    counter = 0
    vidcap = cv2.VideoCapture(pathIn)
    print(type(vidcap)

    if sel_type == 'n_frames':
        # Get fps, total frames. note: fps can be set in the camera.
        total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        #fps = int(vidcap.get(cv2.CAP_PROP_FPS))

        # Generate desired frames
        frames = np.linspace(0, total_frames, n_frames)
        frames = np.around(frames).astype(int)
        #frame_no = ( n_frames /(total_frames))
    
    elif sel_type == 'time':
        #TODO: think of possible ways of getting deried frames/images
        pass

    for pic in frames:

        # reading from frame
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, pic)
        success,image = vidcap.read() 
        #print(success, image)
        if success:
            # if video is still left continue creating images 
            name = pathOut + '/image_' + str(counter) + '.jpg'
            print ('Creating...' + name) 

            # writing the extracted images 
            cv2.imwrite(name, image)
            # increasing counter so that it will 
            # show how many images are created 
            counter += 1
        else:
            print('ABORTED')
            break
    print('Number of images generated: \n', counter)
    vidcap.release() 
    cv2.destroyAllWindows() 



# PARAMETERS
n_frames = 10
width = 1
height = 0.3
v_shift = 0

# Path handling
base_path = r"J:\39 LIVIT ORGANIZATION\1. INVESTIGATIONS\TC_study_automatization\data"
try: 
    # creating a folder named data 
    if not os.path.exists(base_path + '/data'): 
        os.makedirs(base_path + '/data') 
except OSError:
    # if not created then raise error 
    print ('Error: Creating directory of data') 


namein = base_path +'/image_0.avi'
print(namein)
pathout = base_path + '/data'
print(pathout)

extractImages(namein, pathout, n_frames)

# Release all space and windows once done 

