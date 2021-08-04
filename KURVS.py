from astropy.io import fits
import numpy as np 
import matplotlib.pyplot as plt
import statistics
from scipy.optimize import curve_fit
import math



def openData():
    # --- THIS CODE OPENS THE FILE 2D DATA AND RETURNS IT ---
    image = fits.open("/Users/thoma/Desktop/cdfs_30267_cube_median_sub_2d.fits")
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
        brightnessArray = np.array(brightnessList)
    return brightnessList, brightnessArray



def averageBrightness(brightnessList, brightnessArray):
    # --- THIS CODE IS TO AVERAGE THE BRIGHTNESS OF THE LIST OF DATA ---
    print("\n Brightness data:")
    print(brightnessList)
    print("\n Brightness data (Array):")
    print(brightnessArray)
    print("\n Average brightness:")
    print(sum(brightnessList) / len(brightnessList))
    


def writeToGraph(brightnessArray, data): 
    # --- THIS CODE IS FOR WRTITING THE ARRAY DATA TO A SCATTER GRAPH ---
    print("Write to graph")
    xpoints = np.arange(0, data.shape[1], 1)
    ypoints = brightnessArray
    plt.plot(xpoints, ypoints)
    plt.show()



def gaussian(xValues, Amp, mean, sd):
    # --- THIS CODE IS FOR PASSING THE EQUATION OF A GAUGISAN INTO "writeToGaussian" ---
    return  Amp*np.exp(-(xValues-mean)**2/(2.*sd**2)) #this is the equation of a normal curve / gaussian 



def writeToGaussian(brightnessList):
    xdata = np.array(range(0, len(brightnessList))) #this creates an array of numbers in this length 0 - the length of the list
    passedData, pcov = curve_fit(gaussian, xdata, brightnessList) #this returns a list of values to be fit to the curve (mean) 
    plt.plot(xdata, gaussian(xdata, *passedData)) #this passes all of the 
    plt.scatter(xdata, brightnessList)
    plt.show()



def removeHorizontalErrors(data):
    # --- THIS CODE REMOVES THE HORIZONTAL ERRORS FROM THE DATA SET, CAUSED BY INSTRUMENT ERRORS ---
    errorRows = []
    print("Standard Deviation of lines:")
    for y in range(data.shape[0]): # this controlls the vertical, y, direction
        row = []
        for x in range(data.shape[1]): # this controlls the horizontal, x, direction
            row.append(data[y,x]) #appends data to rows for std 
        print(statistics.stdev(row)) # checking
        if statistics.stdev(row) >= 10**-15: # start of working out if row should be removed
            errorRows.append(y)
    print(errorRows)
    data = np.delete(data, errorRows, 0) # removes the rows that have been identified as bad rows.
    print(data)
    return data



def removeVerticalErrors(data):
    # --- THIS CODE REMOVES THE VERTICAL ERRORS FROM THE DATA SET, CAUSED BY THE ATMOSPHERE ---
    errorColumns = []
    print("Standard Deviation of lines:")
    for x in range(data.shape[1]):# this controlls the horizontal, x, direction
        column = []
        for y in range(data.shape[0]):  # this controlls the vertical, y, direction
            column.append(data[y,x]) #appends data to rows for std 
        print(statistics.stdev(column)) # checking
        if statistics.stdev(column) >= 10**-16: # start of working out if row should be removed
            errorColumns.append(x)
    print("These are the columns with errors")
    print(errorColumns)
    data = np.delete(data, errorColumns, 0) # removes the rows that have been identified as bad rows.
    print(data)
    return data



def main():
    data = openData()
    cleandata = removeHorizontalErrors(data)
    cleanestdata = removeVerticalErrors(cleandata)
    brightnessList, brightnessArray = twoDtooneD(cleanestdata)
    writeToGaussian(brightnessList)
    #writeToGaussian(brightnessList, cleandata)
    #writeToGraph(brightnessArray, cleandata )
    #averageBrightness(brightnessList, brightnessArray)
    #writeToGraph(brightnessArray, data)



if __name__ == "__main__":
    print("Running Programn")
    main()
