import math
import pandas as pd

regions = 6

df = pd.read_csv(r'D:\battery_aging\discharge.csv')
voltageLevels = len(df['Voltage_measured']) 
SOC = df['Voltage_measured']
N = int(len(SOC[0:178]))

DP = [['NaN']*N]*regions

def calculateSlope(y, x):
    n = len(x)
    slope = []
    slopeSum = [0]
    for i in range(1, n):
        tempSlope = (y[i] - y[i-1])/(x[i] - x[i-1])
        slope.append(tempSlope)
        slopeSum.append(slopeSum[-1] + abs(tempSlope))
    return slopeSum, slope 

def calculateError(slopeSum, start, end):
    if(start == end):
        return 0
    slopeExp = abs(df['Voltage_measured'][end] - df['Voltage_measured'][start])/(SOC[end] - SOC[start])
    slopeObs = (slopeSum[end] - slopeSum[start])/(end - start)
    error = abs(slopeExp - slopeObs)*(end - start)
    return error
    
    
def REGION_SPLITTER(currIndex, level, N, slopeSum, regStart):
    
    if(level == 0):
        start = regStart
        end = N
        error = calculateError(slopeSum, start, end)
        return error
    
    if(currIndex >= N):
        start = regStart
        end = N 
        error = calculateError(slopeSum, start, end)
        return error
    
    if(DP[level][N] != 'NaN'):
        return DP[level][currIndex]
    
    localError = calculateError(slopeSum, regStart, currIndex)
    error = min(REGION_SPLITTER(currIndex + 1, level - 1, N, slopeSum, currIndex ) + localError, REGION_SPLITTER(currIndex + 1, level, N, slopeSum, regStart))
    DP[level][N] = error
    print(level, N, "   ", end ="")
    return error

slopeSum, slope = calculateSlope(df['Voltage_measured'], SOC)

REGION_SPLITTER(0, regions-1, N-1, slopeSum, 0)