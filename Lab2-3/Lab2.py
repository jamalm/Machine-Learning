import pandas as pd
import numpy
import matplotlib.pyplot
import os

"""
Author: Jamal Mahmoud, C13730921
Date:   01/02/2017
Desc:   This program collects a dataset
        and runs statistical analysis on it to
        produce a Data Quality Report

"""


def main():
    # File Locations
    dataFile = '.\data\DataSet.txt'
    headerFile = r'.\data\featureNames.txt'

    """gets header names"""
    f = open(headerFile, 'r')
    header = f.read().splitlines()
    f.close()

    """gets file as a csv"""
    dataFrame = GetRawCSV(dataFile, header)

    """Split dataframe into continuous and categorical features"""
    # hardcoded columns for continuous and categorical
    splice = [[1, 9, 10, 11, 12, 13, 16, 18, 19, 20, 21, 22, 23, 24, 25], [0, 2, 3, 4, 5, 6, 7, 8, 14, 15, 17]]

    # pass in indices and dataframe to be spliced
    featureSplit = SpliceFeatures(dataFrame, splice)

    """Create DQR's for continuous and Categorical Features"""
    Cont_Report = ContinuousFeatures(featureSplit[0])
    Cat_Report = CategoricalFeatures(featureSplit[1])

    """ Export file to reports directory as csv/txt"""
    Cont_Report.to_csv('./reports/c13730921Continuous.txt')
    Cat_Report.to_csv('./reports/c13730921Categorical.txt')


"""---------------Continuous Features---------------------------"""


# method to prepare continuous feature DQR
def ContinuousFeatures(dataFrame):
    # columns in DQR
    minimum = []
    card = []
    count = []
    missPercent = []
    quart1 = []
    mean = []
    median = []
    quart3 = []
    maximum = []
    sd = []

    # populate columns in DQR
    for i in dataFrame.columns:
        count.append(len(dataFrame[i]))
        dataFrame[i] = CleanData(dataFrame[i], "?")
        dataFrame[i] = dataFrame[i].apply(float)

        missing = len(dataFrame[i]) - dataFrame[i].count()
        missPercent.append(percentage(missing, len(dataFrame[i])))

        minimum.append(dataFrame[i].min())
        card.append(Cardinality(dataFrame[i]))
        mean.append(dataFrame[i].mean())
        median.append(dataFrame[i].median())
        maximum.append(dataFrame[i].max())
        sd.append(dataFrame[i].std())
        quart1.append(dataFrame[i].quantile(0.25))
        quart3.append(dataFrame[i].quantile(0.75))

    # zip data together and create dataframe with column names
    dataSet = list(zip(count, missPercent, card, minimum, quart1, mean, median, quart3, maximum, sd))
    columnSet = ['count', 'Missing Percentage', 'Cardinality', 'Minimum', '1st Quartile', 'Mean', 'Median',
                 '3rd Quartile', 'Maximum', 'Standard Deviation']

    df = pd.DataFrame(data=dataSet, index=dataFrame.columns, columns=columnSet)
    return df


"""----------------- Categorical Features -------------------"""


def CategoricalFeatures(dataFrame):
    count = []
    mode = []
    modePercent = []
    modeFreq = []
    mode2 = []
    mode2Percent = []
    mode2Freq = []
    missPercent = []
    card = []

    for i in dataFrame.columns:
        count.append(len(dataFrame[i]))
        # replaces missing data with NaN values
        dataFrame[i] = CleanData(dataFrame[i], "?")

        missing = len(dataFrame[i]) - dataFrame[i].count()
        print missing
        missPercent.append(percentage(missing, len(dataFrame[i])))

        mode.append(Mode(dataFrame[i], 0))
        modeFreq.append(FrequencyMode(0, dataFrame[i]))
        modePercent.append(percentage(FrequencyMode(0, dataFrame[i]), len(dataFrame[i])))

        mode2.append(Mode(dataFrame[i], 1))
        mode2Freq.append(FrequencyMode(1, dataFrame[i]))
        mode2Percent.append(percentage(FrequencyMode(1, dataFrame[i]), len(dataFrame[i])))
        card.append(Cardinality(dataFrame[i]))
    # print count
    # print missPercent
    # print dataFrame['num-of-doors']

    dataSet = list(zip(count, missPercent, card, mode, modeFreq, modePercent, mode2, mode2Freq, mode2Percent))
    columnSet = ['Count', 'Missing Percentage', 'Cardinality', 'Mode', 'Mode Frequency', 'Mode Percentage', '2nd Mode',
                 '2nd Mode Frequency', '2nd Mode Percentage']
    df = pd.DataFrame(data=dataSet, index=dataFrame.columns, columns=columnSet)
    # print df
    return df


"""Some functions to keep methods clean"""


# splits up continuous and categorical data
def SpliceFeatures(dataFrame, splice):
    # splice dataframe into 2 tables
    continuous = dataFrame.iloc[:, splice[0]]
    categorical = dataFrame.iloc[:, splice[1]]
    return [continuous, categorical]


# percentage function to keep methods clean
def percentage(part, whole):
    return 100 * float(part) / float(whole)


def Cardinality(dataFrame):
    return str(len(dataFrame.unique()))


def CleanData(dataFrame, character):
    return dataFrame.replace("?", numpy.nan)


def FrequencyMode(mode, dataFrame):
    commonValues = dataFrame.value_counts()

    return commonValues.iloc[mode]

def Mode(dataSet, mode):
    commonValue = dataSet.value_counts()
    return commonValue.index[mode]

# reads txt file from data folder adn returns it as a pandas.DataFrame
def GetRawCSV(path, header):
    return pd.read_csv(path, names=header)


if __name__ == '__main__':
    main()
