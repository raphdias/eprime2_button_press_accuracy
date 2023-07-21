import os
import pandas as pd

# Note: The logic here is very rough, but this is for 
# the purpose of being thorough, not efficient. 

# [calculate_acuraccy_from_edat2] output a .csv file 
# compiled of scores for each file that was passed through
def calculate_acuraccy_from_edat2(folderPath):

    fileNames = os.listdir(folderPath)

    """"
    Important Notes For The CSV file 

    Standard1.ACC[Block]   => Standard (Accuracy) 
    Standard1.RT[Block]    => Standard (Response Time)

    Standard1.ACC[Trial]   => 2 Standards before the deviant (Accuracy)
    Standard1.RT[Trial]    => 2 Standard before (Response Time)

    Deviant1.ACC           => All the Deviants (Accuracy)
    Deviant1.RT            => Deviant (Response Time)

    """

    scoresList = []
    rtList = []
    fileNameList = []
    for fileName in fileNames:
        # print(fileName)
        newCSV = folderPath + "/" + fileName
        df = pd.read_csv(newCSV)
        # Setting the column headers to the first row since 
        # it is formatted wrong in the original file
        if (fileName != "2001-1.csv" or fileName != "1001-2.csv"):
            newHeader = df.iloc[0]
            df = df[1:]
            df.columns = newHeader

        try: 
            colNames = ["Standard1.ACC[Block]","Deviant1.ACC","Standard1.ACC[Trial]"]
            stdScore = 0
            devScore = 0
            stdBeforeDevScore = 0
            # For Standard1.ACC[Trial], we are taking the standard before the deviant
            # But it counts every 2 standards before, so we want to count the
            # standard before to the score for Standard1.ACC[Trial]
            # and the standard 2 before to the Standard1.ACC[Block]
            standard2Before = False; 

            for colName in colNames:
                total = 0 
                score = 0 
                df[colName] = df[colName].dropna()
                for x in range(len(df[colName])): 
                    # Checking for str type, since NaN comes back as float
                    if (isinstance(df[colName][x+1], str)):
                        if df[colName][x+1] == "1": 
                            # if we are on the Standard1.ACC[Trial]
                            # Scores are calculated differently
                            if (colName == colNames[2]):
                                # If we have already passed the standard2Before, 
                                # We are on the standard before the deviant
                                if (standard2Before): 
                                    stdBeforeDevScore+=1
                                    standard2Before = False; 
                                # else, it is the normal standard score, 
                                else: 
                                    stdScore+=1; 
                                    standard2Before = True; 
                            elif (colName == colNames[0]):
                                stdScore+=1
                            else: 
                                devScore+=1
                            # Increment total score
                            total+=1
                        elif df[colName][x+1] == "0": 
                            # still have to check for standard before if Standard1.ACC[Trial]
                            if (colName == colNames[2]):
                                # If we have already passed the standard2Before, 
                                # We are on the standard before the deviant
                                if (standard2Before): 
                                    standard2Before = False; 
                                else: 
                                    standard2Before = True; 
                            total+=1
        except: 
            print("Something went wrong with - " + fileName)
        
        # I know this is unintegrated and should definetly be optimized...
        # but response time are calculated using a different method for now

        try: 
            colNamesRT = ["Standard1.RT[Block]","Deviant1.RT","Standard1.RT[Trial]"]
        # Standard in total are 210
        # Deviant in total are 45

            standardsColumnRT = df[colNamesRT[0]].dropna().astype("int").tolist()
            deviantsColumnRT = df[colNamesRT[1]].dropna().astype("int").tolist()
            standardBeforeDeviantColumnRT  = df[colNamesRT[2]].dropna().astype("int").tolist()

            twoBeforeDeviantColumn = df[colNames[2]]

            standardResponseTime = 0 
            deviantsResponseTime = 0 
            totalStd = 0 
            standardBeforeDeviantResponseTime = 0 
            stbdTotal = 0 
            for x in range(len(standardsColumnRT)):
                totalStd += 1
                standardResponseTime += standardsColumnRT[x]
            for x in range(len(deviantsColumnRT)):
                deviantsResponseTime += deviantsColumnRT[x]
            for x in range(len(standardBeforeDeviantColumnRT)):
                if x % 2 == 0: 
                    totalStd += 1
                    # append Response time to standard 
                    standardResponseTime += standardsColumnRT[x]
                else:
                    standardBeforeDeviantResponseTime += standardBeforeDeviantColumnRT[x]
                    stbdTotal += 1

            standardAverageRT = round(standardResponseTime / totalStd, 1)
            deviantAverageRT = round(deviantsResponseTime / len(deviantsColumnRT), 1)
            standardBeforeDeviantAverageRT = round(standardBeforeDeviantResponseTime / stbdTotal, 1)
                # grabbing all the standards
            standardsColumn = df[colNames[0]]
        except: 
            print("(2) Something went wrong with - " + fileName)
        
        scoresList.append([stdScore,devScore,stdBeforeDevScore])
        rtList.append([standardAverageRT, deviantAverageRT, standardBeforeDeviantAverageRT])
        fileNameList.append(fileName)
        finalDictionary = {}
        print(fileNameList)
        for x in range(len(fileNameList)):
            finalDictionary[fileNameList[x]] = scoresList[x]
            finalDictionary[fileNameList[x] + "RT"] = rtList[x]

        return finalDictionary

def mapToCsv(finalDictionary): 

    dfFinal = pd.DataFrame(finalDictionary)
    dfFinal.index = ["Standards", "Deviants", "Std_Before_Dev"]
    dfFinal.to_excel("Harwood_ButtonPress_Accuracy_ordered.xlsx")


if __name__ == "__main__":
    scoreMap = calculate_acuraccy_from_edat2('acc_final')
    mapToCsv(scoreMap)
    print("Score Function Completed -- ")
    print(f"Calculated accross {len(scoreMap.keys())} files")





    
