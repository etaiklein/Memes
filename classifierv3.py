from nGrammer import *


#takes a string and returns the meme it is most similar to. 
#This version uses nGram probabilities
def classifyThis(String, nGramNumber, myMemeTitles, Sigma):
    
    #calculates prior probabilities based on frequency of memes
    priorProbs = countPriorProbabilities(myMemeTitles)
    
    #creates an ngram distribution of the string
    stringNgram = wordDistributionSigma(String.lower().split(" "), nGramNumber, Sigma)
    
    #creates probabilities for the ngrams of each meme
    wordDistribPerTitle = pickedTitleDistribution(nGramNumber, myMemeTitles, Sigma, stringNgram)
    
    #find the probability that a sentance is a meme for all memes, take the highest probability
    bestProbability = 0
    myMeme = "none"    
    
    #for each meme
    for meme in priorProbs.keys():
        
        myprob = 0
        
        #run through the probabilities of each ngram, match to stringNgrams
        for ngram in stringNgram.items():
            
            if meme in wordDistribPerTitle:

                if ngram[0] in wordDistribPerTitle[meme]:
                    #if it is the same as a string nGram add that probability to myProb
                    myprob += wordDistribPerTitle[meme][ngram[0]]
                    
        #balances by multiplying the probabilities of the ngrams by the prior probabilities
        myprob = myprob * (priorProbs[meme]) 
        if myprob > bestProbability:
            bestProbability = myprob
            myMeme = meme
            
        #multiply the resulting probability by the prior probability for that meme and, if it's larger than
        #our largest probability, it becomes our largest probability. Return the meme with the largest probability
    
    return myMeme


#creates a smoothed a balanced ngram probability for each meme type
def pickedTitleDistribution(nGramNumber, myMemeTitles, Sigma, mystringNgram):
    
    mytitles = []
    
    #takes the title and not other information
    for item in myMemeTitles.split(","):
        mytitles.append(item.strip(" "))
    
    #opens the file and makes a list of the titles
    with open("Sample.txt", "r") as f:
        titles = f.readlines()
        
        adict = {}
        
        #gets the name for each meme
        for title in titles:
            memename = title.split(" - ")[0]
            
            #if the meme is in my title
            if memename in mytitles:
                
                #gets the content of each, ignoring splits between the top and bottom
                memecontent = title.split(" - ")[1].strip("*^* ")
                
                #creates nGrams for each title
                if memename not in adict:
                    words = makeNGram(memecontent.split(" "), nGramNumber)
                    adict[memename] = words
                else:
                    words += makeNGram(memecontent.split(" "), nGramNumber)
                    adict[memename] = words
            
                #counts their frequency
                wordlistDict = listCounter(adict.get(memename))
                
                testDataDict = augmentCounter(mystringNgram, wordlistDict)
                
                #addsigma smooths the counter
                testDataDict = augmentCounterSigma(testDataDict, Sigma)
                
                #counts the frequency of its context
                countDict = contextCounter(testDataDict)
                #dictionary for the distribution to be added to
                distributionlist = {}
                
                #adds the frequency of the word in respect to how many contexts it could have appeared in.
                for item in adict.get(memename):
                    distributionlist[item] = (testDataDict[item] / float(countDict[item[1]]))
                
                adict[memename] = distributionlist
                
        return adict

#run is an easy way to use the above functions using user input.
# It also allows an option to compare your sentence to a random number of memes 
def run(testData = "", ngramnumber = 0, number = "" ):
    
    if testData == "":
        testData = raw_input("Enter a sentence to be evaluated :")
        
    if ngramnumber == 0:
        ngramnumber = raw_input("Enter an ngram number (1,2 or 3 recommended) :")
        assert ngramnumber > 0
    
    if number == "":
        while (type(number) != type(1)):
            number = input("Enter a number for a random selection of n memes :")
                
    #chooses n memes to pick between
    memes = pickRandomMemes(int(number))
    
    #renders them in an easily readable form
    printable = []
    for meme in memes.split(", "):
        printable.append(meme.replace("-"," ").strip("\n").strip("/").strip(",").strip())
    
    print "picked memes: " + str(printable)
    
    with open("SampleTypes.txt", "r") as f:
        allmemes = f.readlines()
        
        print "thinking...."
        
        mymeme = classifyThis(testData, int(ngramnumber), memes, .5)
        
        if mymeme != "none":
            print "\"" + testData + "\" is most likely a " + mymeme.replace("-"," ").strip("/").strip() + " meme\n"
                        
            newData = raw_input("Try with different memes? (type yes to continue):")
            
            if newData == "yes":
                run(testData, ngramnumber)
        else:
            print testData + " is equally likely to be any of these memes. " +\
            "Try decreasing the ngram number or entering a longer string"
            
            newData = raw_input("type yes to try again or anything else to quit")
            if newData == "yes":
                run()
        
        print "goodbye\n"

#this function picks a random n number of meme types from the list to use
def pickRandomMemes(number):
    with open("SampleTypes.txt", "r") as f:
        allmemes = f.readlines()
        assert len(allmemes) > number
    
        memelist = []
        
        for item in allmemes:
            item = item.strip("\n")
            memelist.append(item)
            
        mylist = []
        
        while (len(mylist) < number):
            mychoice = choice(memelist)
            memelist.remove(mychoice)
            mylist.append(mychoice)
        
        mystring = ""
        for item in mylist:
            if mystring == "":
                mystring = item
            else:
                mystring += ", " + item
        
        return mystring