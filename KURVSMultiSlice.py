from KURVS import * 



def horizontalLinesErrors(data):
    # --- THIS CODE REMOVES THE HORIZONTAL ERRORS FROM THE DATA SET, CAUSED BY INSTRUMENT ERRORS ---
    errorRows = []
    slices = []
    #print("Standard Deviation of lines:")
    for y in range(data.shape[0]): # this controlls the vertical, y, direction
        row = []
        for x in range(data.shape[1]): # this controlls the horizontal, x, direction
            row.append(data[y,x]) #appends data to rows for std 
        #print(statistics.stdev(row)) # checking the sd
        if statistics.stdev(row) >= 10**-15: # start of working out if row should be removed
            errorRows.append(y)
        # if the y value of a row is in error rows then start a new slice or end an old one and return the correct y values to slice the row between. 
    print(errorRows)
    return errorRows



def splitSlices(data, errorRows):
    cleanData = []
    slices = []
    for y in range(data.shape[0]):     
        if y not in errorRows:
            cleanData.append(y)  
    for row in cleanData:
        startOfSlice = cleanData[0]
        if row + 1 not in cleanData:
            endOfSlice = row
            if startOfSlice != endOfSlice:
                slice = data[startOfSlice: endOfSlice+1, :]
                slices.append(slice)
            cleanData =  cleanData[cleanData.index(row)+1 :]
    return slices

    
def sumEachSlice(slices): 
    sliceSums = []
    for wavelengthSlice in slices:
        sliceSums.append(twoDtooneD(wavelengthSlice))

    return sliceSums
       
        

def createGaussian(sliceSums):
    for array in sliceSums:
        params = writeToGaussian(array)



def main():
    data = openData()
    errorRows = horizontalLinesErrors(data)
    cleandata = removeVerticalErrors(data)
    slices = splitSlices(cleandata, errorRows)
    sliceSums = sumEachSlice(slices)
    print(sliceSums)
    createGaussian(sliceSums) #Why do I have a 3D array? 



if __name__ == "__main__":
    print("Running Programn")
    main()