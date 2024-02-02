#Mahi
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../LLaMa')) # Gets the directory of LLaMaInterface module for import
sys.path.append(os.path.join(os.path.dirname(__file__), '../../Modules')) # Gets the directory of LLaMaInterface module for import

from LLaMaInterface import separateCellHeaders
from LocationInterface import getLongLat
from DiseaseHeader import detectDiseases
from datetime import datetime,timedelta
from typing import *

latLongDict = {
    "Colombo" : ["6.9271N","79.8612E"],
    "Gampaha" : ["7.0840N", "80.0098E"],
    "Kalutara" : ["6.5854N","79.9607E"],
    "Kandy" : ["7.2906N","80.6337E"],
    "Matale" : ["7.4675N","80.6234E"],
    "NuwaraEliya" : ["6.9497N","80.7891E"]
}

'''
Table format: [Disease Name][Cases][Location Name][Lattitude][Longitude][Region Type(City/County/Country)][TimeStampStart][TimeStampEnd]
'''
def convertToTable(importantText: str,timestamps: List[datetime])-> List[str]:
    table = []
    rows = importantText.split('\n')
    labels = detectDiseases(rows[0])
    # if __name__ == '__main__': #for testing
    #     labels = ['RDHS','Dengue Fever','Dysentery','Encephalitis','Enteric Fever','Food Poisoning','Leptospirosis','Typhus','Viral Hepatitis','Human Rabies','Chickenpox','Meningitis','Leishmaniasis','WRCD']
    
    for i in range(2,len(rows)):
        data = rows[i].strip().split(" ")
        locationName = data[0]
        long, lat, regionType = getLongLat(locationName)
        regionType = "Not Found"
        for j in range(1,len(data)-2,2):
            cases = data[j]
            diseaseName = labels[j//2]
            table.append([diseaseName,cases,locationName,lat,long,regionType,timestamps[0].strftime("%Y-%m-%d %H:%M:%S"),timestamps[1].strftime("%Y-%m-%d %H:%M:%S")])
    return table

def printTable(table: List[str])-> None:
    for heading in ['Disease Name','Cases','Location Name','Lattitude','Longitude','RegionType','TimeStampStart','TimeStampEnd']:
        print("|{:<20}".format(heading),end=" ")
    print("|")
    for row in table:
        for col in row:
            print("|{:<20}".format(col),end=" ")
        print("|")


if __name__ == '__main__':
    testData = '''RDHS Dengue Fever Dysentery Encephaliti Enteric Fever Food Poi- Leptospirosis Typhus Viral Hep- Human Chickenpox Meningitis Leishmania- WRCD 
A B A B A B A B A B A B A B A B A B A B A B A B T* C** 
Colombo 412 7733 0 5 0 9 0 1 0 6 7 156 0 0 0 3 0 0 3 151 3 22 0 5 23 100
Gampaha 351 7564 0 7 0 11 0 1 0 2 5 289 0 6 0 9 0 0 3 138 1 36 1 25 1 96 
Kalutara 192 2605 0 14 0 1 0 0 0 5 28 412 0 1 0 2 0 1 6 233 0 40 0 1 8 100 
Kandy 263 2594 0 18 0 0 0 4 0 12 8 132 2 36 0 2 0 1 2 137 0 11 1 15 83 100
Matale 43 723 0 2 0 0 0 1 0 5 4 86 0 9 0 3 0 0 3 30 0 3 5 159 19 100
NuwaraEliya 7 111 4 72 0 1 1 2 0 38 3 53 7 35 1 4 0 0 2 59 0 8 0 0 56 100
Galle 69 1161 3 25 0 11 0 5 0 18 14 492 0 26 0 1 0 1 7 180 0 11 0 1 32 100
Hambantota 82 813 0 4 2 3 0 1 0 8 14 174 2 46 0 7 0 0 1 85 0 14 22 308 22 100
Matara 48 876 2 19 1 6 0 0 2 9 20 317 0 18 0 2 0 1 5 141 1 10 7 87 49 100
Jaffna 51 1527 1 44 0 1 0 8 0 16 0 8 6 463 0 1 0 1 1 110 0 5 0 2 61 93 
Kilinochchi 2 64 0 4 0 0 0 0 0 16 0 7 1 6 0 0 0 0 0 8 0 0 0 0 17 98 
Mannar 4 66 0 6 0 0 0 1 0 0 3 27 0 5 0 0 0 0 0 1 1 4 0 0 26 100
Vavuniya 5 107 0 5 0 1 0 0 0 0 0 25 1 7 0 1 0 0 2 13 0 3 1 6 3 100
Mullaitivu 4 70 0 8 0 0 0 3 0 11 0 26 0 4 0 0 0 0 0 10 0 0 2 5 19 99 
Batticaloa 74 1648 3 127 0 6 0 3 4 16 2 58 0 1 0 3 0 1 2 38 1 23 0 1 53 100
Ampara 0 43 0 1 0 1 0 0 0 0 0 12 0 0 0 1 0 0 0 17 0 7 0 2 15 44 
Trincomalee 77 1704 0 5 0 1 0 0 0 4 2 54 0 13 0 0 0 0 2 30 0 17 0 1 20 100
Kurunegala 123 1673 1 20 0 7 0 0 0 2 19 203 0 9 0 8 0 2 2 255 1 76 8 231 19 100
Puttalam 53 2482 0 7 0 1 0 1 0 0 4 28 0 7 0 1 0 0 1 68 4 32 0 14 15 100
Anuradhapur 48 412 0 3 0 0 0 1 0 2 10 193 1 24 0 2 0 0 5 134 2 25 7 270 20 99 
Polonnaruwa 13 378 0 10 0 5 0 0 0 6 5 115 0 5 0 10 0 0 3 44 0 13 8 227 33 99 
Badulla 17 586 2 17 0 3 0 0 0 26 13 162 0 26 1 58 0 0 9 93 1 21 1 14 64 100
Monaragala 24 320 0 14 1 4 0 0 0 0 21 373 1 28 1 16 0 0 1 40 0 39 5 92 23 100
Ratnapura 82 1127 3 23 0 10 1 2 3 12 39 606 0 16 0 12 0 1 8 101 3 97 5 98 33 100
Kegalle 91 1557 1 12 0 1 0 2 0 8 22 352 1 19 0 3 0 0 5 219 1 33 1 18 28 100
Kalmune 29 1448 3 34 0 7 0 0 0 0 2 30 0 0 0 0 0 0 4 35 1 16 0 0 41 100
SRILANKA 216 39392 23 506 4 90 2 36 9 222 24 4390 22 810 3 149 0 9 77 2370 20 566 74 1582 33 98 '''

    table = convertToTable(testData,[datetime(2023, 6, 9) +timedelta(days=-7),datetime(2023, 6, 9)])
    printTable(table)
