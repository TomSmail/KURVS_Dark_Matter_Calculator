from astropy.io import fits
import numpy as np 
import matplotlib.pyplot as plt
import statistics
from scipy.optimize import curve_fit
import os



def openData():
    # --- THIS CODE OPENS THE FILE 2D DATA AND RETURNS IT ---
    image = fits.open(os.getcwd() + "/cdfs_30267_cube_median_sub_2d.fits")
    data = image[0].data
    return data



def twoDtooneD(data):
    # --- THIS CODE IS TO TURN THE 2D DATA ARRAY INTO A 1D ARRAY ---
    brightnessList = []
    for i in range(data.shape[1]):
        datapoint = 0
        for j in range(data.shape[0]):
            datapoint += data[j,i]
        brightnessList.append(datapoint)
    print(brightnessList)
    return brightnessList



def averageBrightness(brightnessList, brightnessArray):
    # --- THIS CODE IS TO AVERAGE THE BRIGHTNESS OF THE LIST OF DATA AND DISPLAY IT FOR ERROR CHECKING---
    print("\n Brightness data:")
    print(brightnessList)
    print("\n Brightness data (Array):")
    print(brightnessArray)
    print("\n Average brightness:")
    print(sum(brightnessList) / len(brightnessList))
    


def writeToGraph(brightnessArray, data): 
    # --- THIS CODE IS FOR WRTITING THE ARRAY DATA TO A SCATTER GRAPH ---
    xpoints = np.arange(0, data.shape[1], 1)
    ypoints = brightnessArray
    plt.plot(xpoints, ypoints)
    plt.show()



def gaussian(xValues, Amp, mean, sd):
    # --- THIS CODE IS FOR PASSING THE EQUATION OF A GAUGISAN INTO "writeToGaussian" ---
    return  Amp*np.exp(-(xValues-mean)**2/(2.*sd**2)) # this is the equation of a normal curve / gaussian 



def writeToGaussian(instensityList):
    #--- THIS CODE PASSES DATA INTO A FUNCTION WHICH IS THEN USED TO FIT A CURVE, IT ALSO MASKS ALL ROWS THAT DO NOT HAVE USABLE DATA ON THEM ---
    xvalues = np.array(range(0, len(instensityList))) # this creates an array of numbers in this length 0 - the length of the list
    instensityList = instensityList[12:33]
    xdata = [i for i in xvalues if ( i >= 12 and i <= 32)] # this only takes the middle values of each row of xdata 
    passedData, pcov = curve_fit(gaussian, xdata, instensityList, maxfev=100000, p0 = [10**-15, 25, 2]) # this returns a list of values to be fit to the curve (mean) 
    plt.plot(xdata, gaussian(xdata, *passedData)) # this passes all of the attributes from passedData
    plt.scatter(xdata, instensityList)
    plt.show()
    return passedData[1] # this returns the mean of the x values. 



def removeHorizontalErrors(data):
    # --- THIS CODE REMOVES THE HORIZONTAL ERRORS FROM THE DATA SET, CAUSED BY INSTRUMENT ERRORS ---
    errorRows = []
    for y in range(data.shape[0]): # this controlls the vertical, y, direction
        row = []
        for x in range(data.shape[1]): # this controlls the horizontal, x, direction
            row.append(data[y,x]) # appends data to rows for std 
        if statistics.stdev(row) >= 10**-15: # start of working out if row should be removed
            errorRows.append(y)
    data = np.delete(data, errorRows, 0) # removes the rows that have been identified as bad rows.
    return data



def removeVerticalErrors(data):
    # --- THIS CODE REMOVES THE VERTICAL ERRORS FROM THE DATA SET, CAUSED BY THE ATMOSPHERE ---
    for x in range(data.shape[1]):# this controlls the horizontal, x, direction
        column = []
        for y in range(data.shape[0]):  # this controlls the vertical, y, direction
            column.append(data[y,x]) # appends data to rows for std 
        data1 = np.ma.masked_greater(data, 9**-16) # start of working out if row should be removed   
    return data1



def findRedShift(mean):
    meanwavelength = 1.661539031658317 + ((int(mean) -1) * 0.000215820327866822)
    emisionLineHParticle = 0.65628
    redshift = ( meanwavelength - emisionLineHParticle) / emisionLineHParticle
    return redshift, meanwavelength



def main():
    data = openData()
    cleandata = removeHorizontalErrors(data)
    brightnessList = twoDtooneD(cleandata)
    mean = writeToGaussian(brightnessList)
    



if __name__ == "__main__":
    print("Running Programn")
    main()
