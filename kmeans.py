from random import *
import pprint
import ast

#memes are represented in tuples (memename, dictionary of features)
def getMemes():
    with open("SampleFullyDecorated.txt", "r") as f:
        try:
            types = f.readlines()
            
            mymemes = []
            
            for meme in types:
                meme = meme.split(" *dict* ")
                mymemes.append((meme[0], ast.literal_eval(meme[1])))
                           
            return mymemes
        except:
            pass

#method returns a n lists of clustered memes
def mapToMemeList(k = len(getMemes())/10 + 1): 
    mymemes = getMemes()
    initcentroids = randomMemeList(k)
    
    centroids = computeMemes(initcentroids, mymemes)
        
    clusters = []
    
    for meme in centroids:
        clusters.append([])
    
    for meme in mymemes:
            clusters[findClosestMemeIndex(meme[1], centroids)].append(meme[0])
    
    #make it print prettily
    i = 0
    while i < len(clusters):
        
        printable = []
        for item in clusters[i]:
            printable.append(item.replace("-"," ").strip("\n").strip("/").strip(",").strip())
            
        print "Cluster " + str(i) + ": " + str(printable)
        i += 1
        
    return clusters
    
#method to find the index of the list closest to the given meme
def findClosestMemeIndex(target, memeList):
    minIndex = 0
    minDist = computeFeatureDistance(target, memeList[0][1])
    i = 0
    while i < len(memeList):
        dist = computeFeatureDistance(target, memeList[i][1])
        if dist < minDist:
            minIndex = i
            minDist = dist
        
        i += 1
    
    return minIndex
    
    pass

#returns the meme closes to the target meme
def findClosestMeme(target, memeList):
    return memeList[findClosestMemeIndex(target, memeList)]

#meathod to compute the square of the feature distance between two memes
def computeFeatureDistance(MemeDict1, MemeDict2):
    featurelist = MemeDict1.keys()
    distance = 0
    
    for item in featurelist:
        distance += (MemeDict1[item] - MemeDict2[item])*\
        (MemeDict1[item] - MemeDict2[item])
        
    return distance

#method to generate a single random meme with random features
def randomOneMeme():
    newdict = {}
    
    #the following ranges were calculated with computeRanges()
    newdict["wordCount"] = uniform(7.96,21.3)
    newdict["letterRatio"] = uniform(3.70,4.99)
    newdict["countRatio"] = uniform(.362, 3.98)
    
    newdict["thirdPersonWords"] = uniform(0,.008)
    newdict["secondPersonWords"] = uniform(0, 0)
    newdict["firstPersonWords"] = uniform(0, .037)
    newdict["curseCount"] = uniform(0,0)
    newdict["human"] = choice([0,1])
    newdict["gendered"] = choice([0,1])
    newdict["archetype"] = choice([0,1])
    newdict["colorwheel"] = choice([0,1])
    newdict["baitswitch"] = choice([0,1])
    newdict["aligned"] = choice([0,1])
    newdict["aged"] = choice([0,1])
    newdict["drugs"] = choice([0,1])
    newdict["pop"] = choice([0,1])
    newdict["titleCount"] = randint(1,200)
    
    photodrawn = choice([0,1])
    if photodrawn == 0:
        newdict["photo"] = choice([0,1,2])
        newdict["drawn"] = 0
    else:
        newdict["drawn"] = choice([0,1,2])
        newdict["photo"] = 0
    
    return newdict
    
#method to generate a new meme with random features
def randomMemeList(k):

    memeList = []
    
    for i in range(k):
        memeList.append((i,randomOneMeme()))

    return memeList

#uses Kmeans to generate and return a list of representative memes
def computeMemes(centroids, mymemes):
    current = centroids
    mynext = recluster(current, mymemes)
        
    while current != mynext:
        current = mynext
        mynext = recluster(current, mymemes)
    
    return current

#Method to recluster the memes and compute new prototypes
def recluster(currentCentroids, mymemes):
    mynext = []
    clusters = []
    
    for meme in currentCentroids:
        clusters.append([])
    
    for meme in mymemes:
            clusters[findClosestMemeIndex(meme[1], currentCentroids)].append(meme)
    
    i = 0
    for cluster in clusters:
        if cluster != []:
            mynext.append((i, computeCentroid(cluster)))
            i+= 1

            
    return mynext

#Method to compute the centroid meme of a non-empty list of memes
#Memelist is a list of tuples (MemeName, dictionary)
def computeCentroid(MemeList):
    
    startingvalues = {}
    featurelist = MemeList[0][1].keys()
    for item in featurelist:
        startingvalues[item] = 0
    
    for meme in MemeList:
        for item in featurelist:
            startingvalues[item] += meme[1][item]
            
    for item in featurelist:
        startingvalues[item] = startingvalues[item]/len(MemeList)
    
    return startingvalues

#gets the range of values for an entry in a my dictionary
def computeRanges():
    mymemes = getMemes()
    
    for entry in mymemes[1][1].keys():
        
        high = 0
        low = 100
        
        for meme in mymemes:
            if meme[1][entry] > high:
                high = meme[1][entry]
            if meme[1][entry] < low:
                low = meme[1][entry]
                
        print str(entry) + ": high(" + str(high) + ") low (" + str(low) + ")"