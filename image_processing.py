'''
/*
 * @Author: jorgedelpozolerida 
 * @Date: 2020-05-18 15:20:05 
 * @Last Modified by: jorgedelpozolerida
 * @Last Modified time: 2020-05-27 13:04:59
 */
'''

from PIL import Image
import  imghdr
import numpy as np
import glob
import os
from pathlib import Path, PureWindowsPath

def slice_list(input, size):
    input_size = len(input)
    slice_size = int(input_size / size)
    remain = input_size % size
    result = []
    iterator = iter(input)
    for i in range(size):
        result.append([])
        for j in range(slice_size):
            result[i].append(iterator.__next__())
        if remain:
            result[i].append(iterator.__next__())
            remain -= 1
    return result

def image_crop(root, file, left, top, right, bottom, crop_indicator='_crop'):
    '''
    Crops single image in fikle_path as specified by percentages
    left, top, right, bottom.
    Return image with _crop added at the end of filename.
    '''
    try:
        im = Image.open(root + '/' + file)
        # Size of the image in pixels (size of original image)
        width, height = im.size

        # Setting the points for cropped image
        left = int(left*width/100)
        top = (top*height/100)
        right = width - int(right*width/100)
        bottom = height - (bottom*height/100)

        # Cropped image of above dimension
        # (It will not change orginal image)
        im1 = im.crop((left, top, right, bottom))

        # Shows the image in image viewer
        # TODO: select where to save
        file_name, file_ext = os.path.splitext(file)
        n_file = root + '/' + file_name + crop_indicator + file_ext
        im1.save(n_file)
        return True

    except FileNotFoundError:
        # nothing done if file not found/non existing
        print('Image not cropped, error in finding : \n ', file_path)
        return False

def collage_generator(root, files, num_collages=2, crop_indicator='_crop',
                      stack_mode='vertical'):
    '''
    Generates n_collages collages stacking on top images cropped identified by 
    crop_indicator.
    '''
    files = [ file for file in files if imghdr.what(root + '/' + file) is not None]
    files = [file for file in files if crop_indicator in file]
    n_files_total = len(files)
    files = slice_list(files, num_collages)
    for inds, l_file in enumerate(files):
        n_files = len(l_file)
        if n_files != 0:
            try:
                print(l_file)
                # Equal sized images are assumed
                ref_im=Image.open(root + '/' + l_file[0])
                width, height = ref_im.size
                ind_h = 0
                big_im=Image.new('RGB', (width, height*(n_files+1)))
                for ind, file in enumerate(l_file):
                
                    im=Image.open(root + '/' + file)
                    big_im.paste(im, (0, int(ind_h)))
                    ind_h=ind_h+height + height/n_files
                n_file = root + '/' + 'collage' + str(inds) + '.jpg'
                big_im.save(n_file)
            except FileNotFoundError:
                ('Could not find or open a file in: \n', root)
    print('Number of collages generated: ', len(files),
          ' in following folder: \n', root)

def process_images(base_path, left, top, right, bottom, crop_indicator='_crop', 
                    process_mode='crop'):
    '''
    Crops ALL uncropped images found in basepath as specified by left, top,
    right, bottom. Cropped images are identified when they end by _crop

    Args
        base_path: where all folders and images are found
        left: percentage to crop from left
        right : percentage to crop from right
        top: percentage to crop from top
        bottom: percentage to crop from bottom
        crop_indicator : string at the end of file that in dicates images is
        already cropped
    '''
    # Sanity  counters
    counts = 0 
    counts_total = 0
    for root, dirs, files in os.walk(base_path, topdown=True):
        if process_mode == 'crop':
            for file in files:
                file_path = root + '/' + file
                # print(file_path)
                if imghdr.what(file_path) is not None and crop_indicator not in file:
                    counts_total+=1
                    im = image_crop(root, file, left, top, right, bottom, crop_indicator)
                    counts += im
        if process_mode == 'collage':
            collage_generator(root, files, num_collages=2, crop_indicator='_crop',
                              stack_mode='vertical')
    if process_mode == 'crop':
        print('General counts: ', counts_total)
        print('success counts: ', counts )
    print('courtesy of Jorge ;)')


if __name__ == "__main__":
    # Where folders and images are. Cropped files and collages will be added here.
    base_path = r'C:\Users\DelpozoJ\Documents\TC1e'
    # Cropping arguments
    left = 0
    top = 50
    right =  0
    bottom = 10
    process_images(base_path, left, top, right, bottom, crop_indicator='_crop',
                process_mode='crop')
    process_images(base_path, left, top, right, bottom, crop_indicator='_crop',
                    process_mode='collage')
                    