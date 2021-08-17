from KURVS import * 
import matplotlib.pyplot as pyplot



def horizontalLinesErrors(data):
    # --- THIS CODE REMOVES THE HORIZONTAL ERRORS FROM THE DATA SET, CAUSED BY INSTRUMENT ERRORS ---
    errorRows = []
    slices = []
    for y in range(data.shape[0]): # this controlls the vertical, y, direction
        row = []
        for x in range(data.shape[1]): # this controlls the horizontal, x, direction
            row.append(data[y,x]) #appends data to rows for std
        if statistics.stdev(row) >= 10**-15: # start of working out if row should be removed
            errorRows.append(y)
    return errorRows



def splitSlices(data, errorRows):
    # --- THIS CODE SPLITS THE DATA INTO ITS DIFFERENT SLICES USING THE ERROR ROWS THAT WE HAVE PREVIOUSLY WORKED OUT ---
    cleanData = []
    slices = []
    for y in range(data.shape[0]): # this manovers through the y index of the tables
        if y not in errorRows:
            cleanData.append(y)  # this makes sure the data is not anomylous 
    for row in cleanData: # this begins to create slices 
        startOfSlice = cleanData[0]
        if row + 1 not in cleanData:
            endOfSlice = row
            if startOfSlice != endOfSlice:
                slice = data[startOfSlice: endOfSlice+1, :]
                slices.append(slice)
            cleanData =  cleanData[cleanData.index(row)+1 :]
    return slices

    
def sumEachSlice(slices): 
    # --- THIS CODE SUMS EACH INDIVIDUAL SLICE AND RETURNS IT AS A LIST ---
    sliceSums = []
    for wavelengthSlice in slices:
        sliceSums.append(twoDtooneD(wavelengthSlice))
    sliceSums.reverse() # this reverses the list as the data seems to be read from the bottom up
    return sliceSums
       
        

def createGaussian(sliceSums):
    # --- THIS CODE CREATES GRAPHS FOR ALL OF THE SLICES AND ALSO WORKS OUT THE REDSHIFT OF EACH SLICE ---
    redshiftList = []
    lambda_peak_values = []
    for array in sliceSums:
        if 3 <= sliceSums.index(array) <= 10: # only takes the middle slices as outer slices are anomylous
            mean = writeToGaussian(array)
            redshiftList.append(findRedShift(mean))
            lambda_peak_values.append(findRedShift(mean)[1])
    
    return redshiftList, mean, lambda_peak_values



def findDistanceBetweenSlices(slices):
    sliceList = list(range(0, len(slices)))
    mValues = []
    for value in sliceList:
        if 3 <= sliceList.index(value)<= 10: # only takes the middle slices as outer slices are anomylous
            mValues.append(sliceList[value] * 1.72 * 3.086e19) 
    return mValues



def rotationCurve(lambda_peak_values, mValues):
    velocityShifts = []
    referenceWavelength = lambda_peak_values[3] # a wavelength to compare the others to
    for lambda_peak_values in lambda_peak_values:
        velocityShift = 3*10**5*(lambda_peak_values/referenceWavelength - 1)
        velocityShifts.append(velocityShift)
    pyplot.scatter(mValues, velocityShifts, color = "b")
    pyplot.xlabel("Distance from centre of galaxy (km)")
    pyplot.ylabel("Velocity Shift (km/s)")
    pyplot.show()
    return velocityShifts



def correctingInclination(velocityShifts):
    velocityDifferenceMax = velocityShifts[-1] - velocityShifts[0]
    inclinationCorrection = 1.30
    V_rot = velocityDifferenceMax * (inclinationCorrection / 2)
    return V_rot



def findMass(V_rot, mValues):
    # THIS PIECE OF CODE FINDS THE MASS OF A GALAXY GIVEN ITS CORRECTED VELOCITY AND THE DISTANCES FROM THE CENTRE OF THE GALAXY
    R = (mValues[-1] - mValues[0])/2
    V_rot = V_rot * 1000
    Mass = (V_rot**2)*R/(6.67e-11)
    return Mass 



def findDarkMatterFraction(Mass):
    luminousMass = (0.9*10**10)*(1.989*10**30) # this is the solar mass of the galaxy timesed by the number of kilograms in a solar mass 
    darkMatter = Mass - luminousMass 
    darkMatterPercentage = darkMatter/Mass * 100
    print(f"The percentage of dark matter in this galaxy is: {darkMatterPercentage} %")
    return darkMatterPercentage 


def main():
    data = openData()
    errorRows = horizontalLinesErrors(data)
    slices = splitSlices(data, errorRows)
    sliceSums = sumEachSlice(slices)
    mValues = findDistanceBetweenSlices(slices)
    redshiftList, mean, lambda_peak_values = createGaussian(sliceSums)
    velocityShifts = rotationCurve(lambda_peak_values, mValues)
    V_rot = correctingInclination(velocityShifts)
    Mass = findMass(V_rot, mValues)
    findDarkMatterFraction(Mass)




if __name__ == "__main__":
    print("Running Programn")
    main()