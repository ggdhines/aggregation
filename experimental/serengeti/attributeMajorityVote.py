#!/usr/bin/env python
from __future__ import print_function
import os
import csv
import sys

if os.path.exists("/home/ggdhines/github/pyIBCC/python"):
    sys.path.append("/home/ggdhines/github/pyIBCC/python")
else:
    sys.path.append("/Users/greghines/Code/pyIBCC/python")
import ibcc


if os.path.isdir("/Users/greghines/Databases/serengeti"):
    baseDir = "/Users/greghines/Databases/serengeti/"
else:
    baseDir = "/home/ggdhines/Databases/serengeti/"

#species = ['elephant']#,'zebra','warthog','impala','buffalo','wildebeest','gazelleThomsons','dikDik','giraffe','gazelleGrants','lionFemale','baboon','hippopotamus','ostrich','human','otherBird','hartebeest','secretaryBird','hyenaSpotted','mongoose','reedbuck','topi','guineaFowl','eland','aardvark','lionMale','porcupine','koriBustard','bushbuck','hyenaStriped','jackal','cheetah','waterbuck','leopard','reptiles','serval','aardwolf','vervetMonkey','rodents','honeyBadger','batEaredFox','rhinoceros','civet','genet','zorilla','hare','caracal','wildcat']
species = ['gazelleThomsons']
users = []
photos = []


def createConfigFile(classID):
    f = open(baseDir+"ibcc/"+str(classID)+"config.py",'wb')
    print("import numpy as np\nscores = np.array([0,1])", file=f)
    print("nScores = len(scores)", file=f)
    print("nClasses = 2",file=f)
    print("inputFile = '"+baseDir+"ibcc/"+str(classID)+".in'", file=f)
    print("outputFile =  '"+baseDir+"ibcc/"+str(classID)+".out'", file=f)
    print("confMatFile = '"+baseDir+"ibcc/"+str(classID)+".mat'", file=f)
    # if numClasses == 4:
    #     print("alpha0 = np.array([[2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 2], [2, 2,2, 2]])", file=f)
    #     print("nu0 = np.array([25.0, 25.0, 25.0, 1.0])", file=f)
    # elif numClasses == 2:
    #     print("alpha0 = np.array([[2, 1], [1, 2],])", file=f)
    #     print("nu0 = np.array([50.,50.])", file=f)
    # else:
    #     assert(False)
    f.close()


individualClassifications = []
reader = csv.reader(open(baseDir+"filtered20","rU"), delimiter="\t")
for userName, photoName, classification in reader:
    individualClassifications.append((userName,photoName,classification))

ibccClassifications = []



for i, s in enumerate(species):
    votes = {}

    f = open(baseDir+"ibcc/"+str(i)+".in",'wb')
    for userName,photoName,classification in individualClassifications:
        if classification == "[]":
            classification = []
        else:
            classification = [int(v) for v in classification[1:-1].split(",")]

        if not(userName in users):
            users.append(userName)
            userIndex = len(users)-1
        else:
            userIndex = users.index(userName)

        if not(photoName in photos):
            photos.append(photoName)
            photoIndex = len(photos)- 1
        else:
            photoIndex = photos.index(photoName)

        if i in classification:
            if photoIndex in votes:
                votes[photoIndex].append(1)
            else:
                votes[photoIndex] = [1]
        else:
            if photoIndex in votes:
                votes[photoIndex].append(0)
            else:
                votes[photoIndex] = [0]



    #merge the results into the existing ones
    #assume all photos are now in the list - should be
    reader = csv.reader(open(baseDir+"ibcc/"+str(i)+".out","rU"), delimiter=" ")
    for photoIndex in range(len(photos)):
        v = votes[photoIndex]

        if len(ibccClassifications) < (photoIndex+1):
            ibccClassifications.append([])

        if sum(v)/float(len(v)) > 0.5:
            #print(photoIndex,len(ibccClassifications))
            ibccClassifications[photoIndex].append(s)





#next, read in the the experts' classifications
expertClassifications = [[] for p in photos]
print("Reading in expert classification")
reader = csv.reader(open(baseDir+"expert_classifications_raw.csv", "rU"), delimiter=",")
next(reader, None)

for row in reader:
    photoName = row[2]
    photoIndex = photos.index(photoName)
    tagged = row[12]

    if not(tagged in expertClassifications[photoIndex]) and (tagged in species):
        expertClassifications[photoIndex].append(tagged)


total = 0.
correct = 0
for u,e in zip(ibccClassifications,expertClassifications):
    total += 1
    if u == e:
        correct += 1





print(correct/total)
