import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

def unpack(row, kind='td'):
    line = row.findall('.//%s' % kind)
    return [val.text_content() for val in line]

def getStockPrice(fileName):
    price = []
    size = []
    with open(fileName) as f:
        for line in f:
            item = line.rstrip().split(',')
            price.append(float(item[-2]))
            size.append(float(item[-1]))
    return price, size[2:-1]

def getInputData(fileName):        
    fileName = 'data/' + fileName
    price, size = getStockPrice(fileName)
    currentPrice = price[2:-1]
    lastMonthPrice = price[1:-2]
    twoMonthPrice = price[:-3]
    inputData = np.array([currentPrice, lastMonthPrice, twoMonthPrice, size]).T
    return inputData

if __name__ == '__main__':
    unemployment = []
    with open("data/unemployment", 'r') as f:
       for line in f:
           unemployment.append(map(float, line.rstrip().rstrip('\n').split(' ')))
    unemployment = [item for sublist in unemployment for item in sublist]
    
    inflation = []
    with open("data/inflation", 'r') as f:
        for line in f:
            inflation.append(line.rstrip().rstrip('\n').split('   '))
    inflation = map(float, [item.rstrip('%') for sublist in inflation for item in sublist])
    
    djia = []
    with open("data/djia", 'r') as f:
        for line in f:
            djia.append(float(line.rstrip()))
    djia = djia[1:]
    
    sp = []
    with open('data/sp', 'r') as f:
        for line in f:
            item = line.rstrip().split(',')
            sp.append(float(item[-2]))
    sp = sp[1:]
    
    clusterData = np.array([unemployment, inflation, djia, sp]).T
    np.savetxt('data/clusterData.txt', clusterData)
    sampleSize = np.size(clusterData, axis=0)


    priceInfo = getInputData('apple')
    aggData = np.concatenate((priceInfo, clusterData), axis=1)
    columnNames = ['current price', 'past month', '2 month ago',\
        'volume', 'unemploy.', 'inflation', 'DJIA', 'S&P']
    aggData = pd.DataFrame(aggData, columns=columnNames)
    from pandas.plotting import scatter_matrix
    scatter_matrix(aggData, figsize=(12,12))
    plt.savefig("correlationBetweenFeatures.png")
