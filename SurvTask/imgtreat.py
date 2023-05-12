# imgtreat.py>
# Library used for image treatment: all the image deformations are here
# Imported in stimuli as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################

import cv2 as cv
import numpy as np
from scipy.stats import poisson


def gaussiannoise(imghandler, perc=0.0):
    # Gaussian Noise adding to the imagehandler
    # Gaussian Params
    mean = 0
    stddev = perc*100
    # Gaussian Noise Matrix
    gaussian_noise = np.zeros(imghandler.shape,dtype=np.uint8)
    cv.randn(gaussian_noise, mean, stddev)
    # Adding of the matrix on the imagehandler
    outImg = cv.add(imghandler,gaussian_noise)
    return outImg


def saltpeppernoise(imghandler, perc=0.0):
    # Salt-&-Pepper Noise adding to the imagehandler
    # Salt and pepper params
    salt_vs_pepper = perc
    amount = 0.04
    # Salt and Pepper coordinates making
    num_salt = np.ceil(amount * imghandler.size * salt_vs_pepper)
    num_pepper = np.ceil(amount * imghandler.size * (1-salt_vs_pepper))
    salt_coords = [np.random.randint(0,i-1,int(num_salt)) for i in imghandler.shape]
    pepper_coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in imghandler.shape]
    #Change of Pixel Color in the imghandler
    outImg = imghandler.copy()
    outImg[tuple(salt_coords)] = 255
    outImg[tuple(pepper_coords)] = 0
    return outImg


def poissonnoise(imghandler, perc=0.0):
    # Poisson Noise adding to the imagehandler
    # Poisson noise params
    lam = 10*perc
    # Generate Poisson Noise Matrix
    poisson_noise = poisson.rvs(lam, size=imghandler.shape).astype(np.uint8)
    outImg = cv.add(imghandler,poisson_noise)
    return outImg


def specklenoise(imghandler, perc=0.0):
    # Speckle Noise adding to the imagehandler
    # Speckle noise params
    mean = 0
    stddev = 0.1
    # Generate speckle noise matrix
    speckle_noise = np.zeros(imghandler.shape, dtype=np.float64)
    cv.randn(speckle_noise, mean, stddev)
    # Add speckle noise to the matrix
    outImg = imghandler + imghandler * speckle_noise
    outImg = np.clip(outImg, 0, 255).astype(np.uint8)
    return outImg


def blur(imghandler, perc=0.0):
    # Blur effect adding to the imagehandler
    kernels = round(perc*5)
    outImg = cv.blur(imghandler, (kernels,kernels))
    return outImg


def lowcontrast(imghandler, perc=0.0):
    # Low Contrast adding to the imagehandler
    alpha = perc*1.5  # Contrast multiplier
    beta = 0  # Contrast adjustment
    # Generate Low Contrast Image
    outImg = cv.convertScaleAbs(imghandler, alpha=alpha, beta=beta)
    return outImg


def bars(imghandler, perc=0.0):
    # Bars adding to the imagehandler
    # Bars effect params
    intensity = perc
    radius = 1
    # Creating a gaussian Kernel
    sigma = max(imghandler.shape)*radius
    kernel_size = int(2 * np.ceil(3*sigma) + 1)
    kernel = cv.getGaussianKernel(kernel_size, sigma)
    #Adding bars
    blur_mat = cv.filter2D(imghandler, -1, kernel)
    h, w = blur_mat.shape
    r_part = blur_mat[:, w//2:w].copy()
    blur_mat[:, :w//2] = r_part
    blur_mat = cv.rotate(blur_mat, cv.ROTATE_90_CLOCKWISE)
    outImg = cv.addWeighted(imghandler, 1-intensity, blur_mat, intensity, 0)
    return outImg

def vignette(imghandler, perc=0.0):
    # Vignette adding to the imagehandler
    rows, cols = imghandler.shape[:2]
    kernel_x = cv.getGaussianKernel(int(cols), 25)
    kernel_y = cv.getGaussianKernel(int(rows), 25)
    kernel = kernel_y * kernel_x.T
    mask = 255 * (kernel / np.linalg.norm(kernel))
    # Applying Mask
    outImg = imghandler*mask
    return outImg

def tearing(imghandler):
    # Image Tearing effect
    # Tearing params
    num_lines = 8
    line_thick = 3
    # calculate height of each tearing line
    line_height = imghandler.shape[0] // num_lines

    #iterate through tearing lines
    for i in range(num_lines):
        # calculate the y-coord range for the tearing
        y_start = i* line_height
        y_end = y_start + line_thick

        #swap the tearing line with the corresponding section below
        temp = np.copy(imghandler[y_start:y_end, :])
        imghandler[y_start:y_end, :] = imghandler[y_end:y_end + line_thick, :]
        imghandler[y_end:y_end + line_thick, :] = temp

    outImg = imghandler
    return outImg