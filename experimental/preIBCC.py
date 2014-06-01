#!/usr/bin/env python

__author__ = 'ggdhines'
import csv

animal = "wildebeest"
try:
    f = open("/home/ggdhines/aws/2014-05-25_serengeti_classifications.csv", 'rb')
except IOError:
    f = open("/home/ggdhines/Databases/serengeti/filtered.csv", "rb")

reader = csv.reader(f, delimiter=",")

userList = []
photoList = []

userDict = {}
classifications = {}

next(reader, None)
for row in reader:
    userStr = row[1]
    photoStr = row[2]
    speciesStr = row[11]

    try:
        userID = userList.index(userStr)
    except ValueError:
        userList.append(userStr)
        userID = len(userList) -1

    try:
        user = userDict[userID]
    except KeyError:
        userDict[userID] = {}
        user = userDict[userID]

    #check to see if this photo has been tagged at all before
    try:
        photoID = photoList.index(photoStr)
        #if so, get the list of all the users who have tagged (or classified) this photo
        c = classifications[photoID]

        #if this is the first time we've come across this particular user classifying this photo
        if not(userID in c):
            #we've reached the desired max number of users for this photo
            if len(c) > 10:
                continue
            else:
                c.append(userID)

    except ValueError:
        photoList.append(photoStr)
        photoID = len(photoList) - 1
        classifications[photoID] = [userID]

    #has the user already tagged this photo?
    if photoID in user:
        user[photoID] = (speciesStr == animal) or user[photoID]
    else:
        user[photoID] = (speciesStr == animal)

for photoID in classifications:
    for userID in classifications[photoID]:
        if user[photoID] == True:
            f = 1
        else:
            f = 0
        print str(userID) + "," + str(photoID) + "," + str(f)

