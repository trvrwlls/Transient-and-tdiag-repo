import numpy as np
import os 
import matplotlib.pyplot as plt
from PIL import Image 
import pandas as pd
import datetime
from scipy import optimize

# Get the list of transients only the full sets though

# class ExtractData:

#     def __init__(self, startingDate, startingTime, endingDate, endingTime, folderPath, saveLocation):

# print(startingDate, startingTime, endingDate, endingTime)


def ExtractData(startingDate, startingTime, endingDate, endingTime, transFolderPath, 
                tdiagFolderPath, saveLocation): 
    startingDateTime = formatTime(startingDate, startingTime)
    endingDateTime = formatTime(endingDate, endingTime)

    startingDateDir = dateDirPath(startingDate, transFolderPath)
    endingDateDir = dateDirPath(endingDate, transFolderPath)

    transFileList = fileListRecurTrans(os.path.commonpath((startingDateDir, endingDateDir)), transFolderPath, startingDateTime, endingDateTime)

    transPngList = filterTransList(transFileList)

    startingDateDir = dateDirPath(startingDate, tdiagFolderPath)
    endingDateDir = dateDirPath(endingDate, tdiagFolderPath)

    # if tDiagOn: 
    tDiagFileList = fileListRecurTDiag(os.path.commonpath((startingDateDir, endingDateDir)), tdiagFolderPath, startingDateTime, endingDateTime)

    tDiagPngList = filterTDiagList(tDiagFileList)
    # print(tDiagPngList)
    
    readFilesWTDiag(transPngList, tDiagPngList, saveLocation)
    

# builds a list from the transPngList and tDiagPngList like so: trans, trans, trans, tdiag, trans, trans, trans, tdiag,...
def buildList(transList, tDiagList):

    # for i, trans in enumerate(transList):
    i = 0
    N = len(transList) + len(tDiagList)

    arr = []
    j = 0

    
    while i < N:
        # print('i: %i || j: %i || k: %i' % (i, j, ((i+1)//4)))

        # print( )
        if (i+1 ) % 4 == 0:
            arr.append(tDiagList[((i+1)//4)-1])
        else:
            arr.append(transList[j])
            j += 1

        i += 1
    return arr


def formatTime(date, time):
    dateArr = date.split('/')
    timeArr = time.split(':')
    hr = int(timeArr[0])
    min = int(timeArr[1])
    sec = int(timeArr[2])

    dt = datetime.datetime(int(dateArr[2]), int(dateArr[1]), int(dateArr[0]), hr, min, sec)
    
    return dt


def dateDirPath( date, path):
    '''
    date (string) of the form day/month/year needs to be formatted year/month/day then can be appended onto any string
    we can use str.join
    '''
    dateList = date.split('/')
    dateList.reverse()    
    formattedDateDir = path + '\\'+'\\'.join(dateList)
    return formattedDateDir


def readFilesWTDiag(transPngFiles, tDiagPngFiles, saveLocation):

    pngFiles = buildList(transPngFiles, tDiagPngFiles)
    N = len(pngFiles)

    # collage sizing
    imageSize = (904,960)
    imageSizeTDiag = (749, 431)
    transColumns = 3
    columns = 4 

    width = (transColumns if N >= transColumns else N % transColumns) * imageSize[0] + imageSizeTDiag[0]
    height = - (N // - columns) * imageSize[1] # ceiling division
    collageSize = (width, height) # collage dimensions


    collage = Image.new("RGBA", collageSize) # blank image for collage to be drawn on
    
    pointer = [0,0]
    # print(collageSize)

    for i, pngFile in enumerate(pngFiles):
        # print(pngFile0)
        with Image.open(pngFile) as imToAdd:
            # print('hello')
            # print(imToAdd)
            # print( (i+1) % 4 != 0 )
            imToAdd = imToAdd.resize(imageSizeTDiag) if (i+1) % 4 == 0 else imToAdd.resize(imageSize)
            # print(imToAdd.size)

            currentSize = imToAdd.size



            collage.paste(imToAdd, box = pointer.copy())

            # print('init pointer', pointer)
            pointer[0] = (pointer[0] + currentSize[0]) % width
            
            if pointer[0] == 0:
                pointer[1] = pointer[1] + imageSize[1]
            

            imToAdd.close()
            
    startingTimeString = str(formatTimeFromPath(pngFiles[0]).time()).replace(':','_')
    endingTime = formatTimeFromPathTDiag(pngFiles[-1])

    endingDateTime = formatTimeFromPathTDiag(pngFiles[-1])
    endingTimeString = str(endingDateTime.time()).replace(':','_')
    # print(type(endingDateTime.date()),':D')
    # endingTime = str(formatTimeFromPathTDiag(pngFiles[-1]).time()).replace(':','_')
    # print(str(endingDateTime.date()),':D')
    year, month, day = str(endingDateTime.date()).split('-')

    path = r'%s\%s\%s\%s' % (saveLocation, year, month, day)
    # print(path)
    if not os.path.isdir(path):
        os.makedirs(path)
    filePath = r'%s\\Trans Collage %s - %s.png' % (path, startingTimeString, str(endingTime.time()).replace(':','_'))

    collage.save(filePath)
    
    # collage.save('%s\\Trans Collage %s - %s.png' % (saveLocation, startingTimeString, str(endingTime).replace(':','_')))


# def readFiles(pngFiles, saveLocation):
#     # collage dimensions
#     N = len(pngFiles)

#     # collage sizing
#     imageSize = (904,960)
#     columns = 3
#     width = columns * imageSize[0] # testinng whether this is possible

#     # width = (N % 11) * imageSize[0] # testinng whether this is possible
#     width = (columns if N >= columns else N % columns) * imageSize[0]
#     height = - (N // - columns) * imageSize[1] # ceiling division
#     collageSize = (width, height) # collage dimensions

#     collage = Image.new("RGBA", collageSize) # blank image for collage to be drawn on
    
#     for i, pngFile in enumerate(pngFiles):

#         with Image.open(pngFile) as imToAdd:
        
#             imToAdd = imToAdd.resize(imageSize)

#             collage.paste(imToAdd , ((i%columns) * imageSize[0], i//columns * imageSize[1] ))

#             imToAdd.close()
            
#     startingTimeString = str(formatTimeFromPath(pngFiles[0]).time()).replace(':','_')
    
    
#     endingDateTime = formatTimeFromPathTDiag(pngFiles[-1])
#     endingTimeString = str(endingDateTime.time()).replace(':','_')
#     print(type(endingDateTime.date()),':D')

#     # path = r'%s\%s' % (saveLocation, year, month, day)
    
#     # print(path)

#     # it will be the datetime of the final day 
#     collage.show()
#     collage.save('%s\\Trans Collage %s - %s.png' % (saveLocation, startingTimeString, endingTimeString))

def formatTimeFromPath(path):
    # def formatTimeFromPath(self, path):
    splitPath = path.split(os.sep)


    # if option == 0:
    splitList = os.path.basename(path).split(' ')

    # timeArr = splitList[0].split('_') + splitList[1:2]

    year = int(splitPath[-5])
    month = int(splitPath[-4])
    day = int(splitPath[-3])
    timeArr = splitList[1].split('_')


    hr = int(timeArr[0])
    min = int(timeArr[1])
    secList = timeArr[2].split('.')
    sec = int(secList[0])
    
    ms = int(secList[1])*10000

    # time = datetime.datetime(year, month, day, hr, min, sec, ms)

    time = datetime.datetime(year, month, day, hr, min, sec)
    return time



def formatTimeFromPathTDiag(path):
 
    splitPath = path.split(os.sep)


    year = int(splitPath[-4])
    month = int(splitPath[-3])
    day = int(splitPath[-2])



    timeArr = os.path.basename(path).split('_')[3:5]

    hr = int(timeArr[0][:2])
    min = int(timeArr[0][2:])
    sec = int(timeArr[1].split('.')[0])

    time = datetime.datetime(year, month, day, hr, min, sec)

    return time

def fileListRecurTDiag( commonPath, givenPath, startingDate, endingDate, arr = np.array([])):

    for head in os.listdir(commonPath):
        path = os.path.join(commonPath, head) 
        
        if os.path.isdir(path) and head.isnumeric():
            
            splitPath = path.split('\\')
        
            splitGiven = givenPath.split('\\')
            
            datelist1 = [int(split) for split in splitPath if not split in splitGiven]

            
            if len(datelist1) == 1 and (startingDate.year <= datelist1[0] and datelist1[0] <= endingDate.year):

                arr = np.append(arr , fileListRecurTrans(path, givenPath, startingDate, endingDate))
                
            elif len(datelist1) == 2 and (startingDate.year <= datelist1[0] and datelist1[0] <= endingDate.year) and (startingDate.month <= datelist1[1] and datelist1[1] <= endingDate.month) :
                
                arr = np.append(arr , fileListRecurTrans(path, givenPath, startingDate, endingDate))

            elif len(datelist1) == 3 and (startingDate.year <= datelist1[0] and datelist1[0] <= endingDate.year) and (startingDate.month <= datelist1[1] and datelist1[1] <= endingDate.month) and (startingDate.day <= datelist1[2] and datelist1[2] <= endingDate.day):

                arr = np.append(arr , fileListRecurTrans(path, givenPath, startingDate, endingDate))


        # elif os.path.isfile(path) and (('.png' in head and not 'particles' in head ) or '.alg' in head):
        elif os.path.isfile(path) and ('.png' in head and 'anal' in head and not 'AllTemps' in head): # the anal stands for analysis
            # print(path)
            # now i believe im going to need turn this into a datetime but we will see
            date = formatTimeFromPathTDiag(path)
            if startingDate <= date and date <= endingDate:
                arr = np.append(arr , path)
        

    return arr

# this is by far my favourite piece of code i have made in a while
def fileListRecurTrans( commonPath, givenPath, startingDate, endingDate, arr = np.array([])):

    for head in os.listdir(commonPath):
        path = os.path.join(commonPath, head) 
        # print(path)
        
        if os.path.isdir(path) and head.isnumeric():
            
            splitPath = path.split('\\')
        
            splitGiven = givenPath.split('\\')
            
            datelist1 = [int(split) for split in splitPath if not split in splitGiven]

            
            if len(datelist1) == 1 and (startingDate.year <= datelist1[0] and datelist1[0] <= endingDate.year):

                arr = np.append(arr , fileListRecurTrans(path, givenPath, startingDate, endingDate))
                
            elif len(datelist1) == 2 and (startingDate.year <= datelist1[0] and datelist1[0] <= endingDate.year) and (startingDate.month <= datelist1[1] and datelist1[1] <= endingDate.month) :
                
                arr = np.append(arr , fileListRecurTrans(path, givenPath, startingDate, endingDate))

            elif len(datelist1) == 3 and (startingDate.year <= datelist1[0] and datelist1[0] <= endingDate.year) and (startingDate.month <= datelist1[1] and datelist1[1] <= endingDate.month) and (startingDate.day <= datelist1[2] and datelist1[2] <= endingDate.day):

                arr = np.append(arr , fileListRecurTrans(path, givenPath, startingDate, endingDate))


        # elif os.path.isfile(path) and (('.png' in head and not 'particles' in head ) or '.alg' in head):
        elif os.path.isfile(path) and ('.png' in head and 'FullSet' in head ):

            # now i believe im going to need turn this into a datetime but we will see
            date = formatTimeFromPath(path)
            if startingDate <= date and date <= endingDate:
                arr = np.append(arr , path)

        elif os.path.isdir(path) and 'TransientPngs' in path:

            arr = np.append(arr , fileListRecurTrans(path, givenPath, startingDate, endingDate))

    return arr
    
def filterTransList(fileList):
    pngList = []
    
    for file in fileList:
        if '.png' in file or 'TransPlot_FullSet' in file:
            pngList.append(file)

    return pngList

def filterTDiagList(fileList):
    pngList = []

    for file in fileList:
        if '.png' in file and 'anal' in file:
            pngList.append(file)

    return pngList
    

if __name__ in '__main__':
    # 11_35_12.01_to_12_33_25.47.png
    
    # path = r'G:\Experiments\ALPHA\PositronData\Autolog\2023\07\18\TransientPngs'
    # path = path + '\\TransPlot_FullSet 07_40_52.95.png'
    # print(formatTimeFromPath(path))
    # path = r'G:\Experiments\ALPHA\Faraday Cup Traces_AT\2023\07\18'
    # path = path + '\\FC_Sig_20230718_0432_54.229_anal'
    # print(formatTimeFromPathTDiag(path))
    


    # startingDate = '18/07/2023'
    # endingDate = '18/07/2023'
    # startingTime = '11:35:00'
    # endingTime = '12:33:30'
    # transFolderPath = r'G:\Experiments\ALPHA\PositronData\Autolog'
    # tDiagFolderPath = r'G:\Experiments\ALPHA\Faraday Cup Traces_AT'
    # savePath = 'C:\\Users\\trwells\\desktop'
    
    startingDate = '17/07/2023'
    endingDate = '17/07/2023'
    startingTime = '22:33:00'
    endingTime = '23:17:30'
    transFolderPath = r'G:\Experiments\ALPHA\PositronData\Autolog'
    tDiagFolderPath = r'G:\Experiments\ALPHA\Faraday Cup Traces_AT'
    savePath = 'C:\\Users\\trwells\\desktop'

    # startingDate = '12/06/2023'
    # endingDate = '12/06/2023'
    # startingTime = '20:57:00'
    # endingTime = '20:58:00'
    # folderPath = 'G:\Experiments\\ALPHA\\MCP_Images_AT'
    # savePath = 'C:\\Users\\trwells\\Desktop'
    ExtractData(startingDate, startingTime, endingDate, endingTime, transFolderPath, tDiagFolderPath, savePath, True)
