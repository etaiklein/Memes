from math import *
from random import *


#counts how many memes are there for each type
def countTitles(mytitles):
    with open("Sample.txt", "r") as f:
        titles = f.readlines()
        adict = {}
            
        for word in titles:
            #looks at only the type of the meme, not the content
            word = str(word).split(" - ")[0]
            if mytitles == []:
                if word not in adict:
                    adict[word] = 1
                else:
                    adict[word] += 1
            else:
                if word in mytitles:
                    if word not in adict:
                        adict[word] = 1
                    else:
                        adict[word] += 1
                 
        return adict

#creates a weighted distribution of the titles (title / total titles)
def countPriorProbabilities(mytitles = []):
        
    adict = countTitles(mytitles)

    total = 0
    #counts their frequency
    for item in adict.items():
        total += item[1]

    #dictionary for the distribution to be added to
    distributionlist = {}
    
    #adds the frequency of the type in respect to how types there are
    for item in adict.items():
        distributionlist[item[0]] = (float(item[1]) / float(total))
            
    return distributionlist

#counts all words for all titles                    
def countAllWords():
    adict = {}
    with open("Sample.txt", "r") as f:
        titles = f.readlines()
        for title in titles:
            title = title.split(" - ")[0]
            words = title.split(" ").strip("*^* ")
            for word in words:
                if word not in adict:
                    adict[word] = 1
                else:
                    adict[word] += 1
             
    return adict
#-------------------

#Creates a dictionary of meme type to ngram frequency of the words in each title of the meme
def makeGlobalDistribution(nGramNumber):
    with open("Sample.txt", "r") as f:
        titles = f.readlines()
        words = []
        
        for title in titles:
            memecontent = title.split(" - ")[1].strip("*^* ").strip()
            
            #creates nGrams for each title
            words += (makeNGram(memecontent.split(" "), nGramNumber))
            
        #counts their frequency
        wordlistDict = listCounter(words)
        #counts the frequency of its context
        countDict = contextCounter(wordlistDict)
        #dictionary for the distribution to be added to
        distributionlist = {}
        
        #adds the frequency of the word in respect to how many contexts it could have appeared in.
        for item in words:
            distributionlist[item] = (wordlistDict[item] / float(countDict[item[1]]))
        
        return distributionlist
        
#creates a dictionary of distributions for each title.
def makeTitleDistribution(nGramNumber):
    with open("Sample.txt", "r") as f:
        titles = f.readlines()
        adict = {}
        for title in titles:
            memename = title.split(" - ")[0]
            memecontent = title.split(" - ")[1].strip("*^* ").strip()
            
            #creates nGrams for each title
            if memename not in adict:
                words = makeNGram(memecontent.split(" "), nGramNumber)
                adict[memename] = words
            else:
                words += makeNGram(memecontent.split(" "), nGramNumber)
                adict[memename] = words
        
            #counts their frequency
            wordlistDict = listCounter(adict.get(memename))
            #counts the frequency of its context
            countDict = contextCounter(wordlistDict)
            #dictionary for the distribution to be added to
            distributionlist = {}
            
            #adds the frequency of the word in respect to how many contexts it could have appeared in.
            for item in adict.get(memename):
                distributionlist[item] = (wordlistDict[item] / float(countDict[item[1]]))
            
            adict[memename] = distributionlist
        return adict


def makeWordlist(adictOfDict, nGramNumber):
    mylist = []
    for adict in adictOfDict.values():
        mylist.append(adict.keys())
    return mylist
    
# counters are pretty self-explanatory
#--------------------------------

def counter(filename):
    words_list = open(filename, "r")

    adict = {}
    
    for word in words_list:
        word = word.strip("\n")
        word = word.strip("")
        if word not in adict:
            adict[word] = 1
        else:
            adict[word] += 1
    return adict


def dictCounter(dictionary):
    words_list = dictionary.items()
    return listCounter(words_list)

def listCounter(words_list):
    
    adict = {}
    for word in words_list:
        if word not in adict:
            adict[word] = 1
        else:
            adict[word] += 1
    
    return adict

def contextCounter(adict):
    contextDict = {}
    for key in adict.items():
        if key[0][1] not in contextDict:
            contextDict[key[0][1]] = key[1]
        else:
            contextDict[key[0][1]] += key[1]
    return contextDict
    


# older functions
#--------------------------------

#rewrites a file where each word is on a new line to be a file where each ngram is on a line 
def makeNGram(newWords, nGramNumber):
    #takes unigrams at minimum
    assert nGramNumber > 0

    nGramWords = []
    
    #iterates through the new list
    j = 0
    #stops when it's run through all the words in the file
    while j < len(newWords):
        #at least, the first word in each file will be by itself
        string = str(newWords[j])
        newString = ""
        n = nGramNumber-1
        while n > 0:
            # words in my text doc will be followed by the n previous words in the given text file
            if (j-n) >= 0:
                newString += str(newWords[j-n])
            if n> 1:
                newString += " "
            n-=1

        nGramWords.append((string.strip("\n").lower(), newString.strip("\n").lower()))
        j+=1
    return nGramWords

def wordDistribution(wordlist, nGramNumber):
    #creates nGrams for the list
    words = makeNGram(wordlist, nGramNumber)
    #counts their frequency
    wordlistDict = listCounter(words)
    
    #counts the frequency of its context
    countDict = contextCounter(wordlistDict)
    #dictionary for the distribution to be added to
    distributionlist = {}
    
    #adds the frequency of the word in respect to how many contexts it could have appeared in.
    for item in words:
        distributionlist[item] = (wordlistDict[item] / float(countDict[item[1]]))
    
    return distributionlist


#word distribution
def wordDistributionSigma(wordlist, nGramNumber, sigma):
    #creates nGrams for the list
    words = makeNGram(wordlist, nGramNumber)
    #counts their frequency
    wordlistDict = listCounter(words)
    
    #addsigma smooths the counter
    wordlistDict = augmentCounterSigma(wordlistDict, sigma)
    
    #counts the frequency of its context
    countDict = contextCounter(wordlistDict)
    #dictionary for the distribution to be added to
    distributionlist = {}

    #adds the frequency of the word in respect to how many contexts it could have appeared in.
    for item in words:
        distributionlist[item] = (wordlistDict[item] / float(countDict[item[1]]))
    
    return distributionlist



#Counter helper functions
#-----------------------------------------------------------------

#adds sigma to all words
def augmentCounterSigma(adict, sigma):
    for word in adict.keys():
        adict[word] += sigma
    
    return adict

#adds new words to the dictionary but doesnt assign a value
def augmentCounter(testData, adict):
    for word in testData:
        if word not in adict:
            adict[word] = 0.0
    
    return adict
