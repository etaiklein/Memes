from nGrammer import *


def makeRandomTrigram(numberOfWords, nGramNumber = 3,):
    
    #creates the probability table
    distribution = makeGlobalDistribution(nGramNumber)
    
    #this function will eventually output a string
    myString = []

    #adds some random words from the list to start with
    #uses a random context that was split to insure that the words have probability.
    randomStartWords = choice(distribution.keys())[1].split(" ") 
    
    #restart if it hits a null context
    if randomStartWords[0] == '':
        randomStartWords = choice(distribution.keys())[1].split(" ") 
        
    for item in randomStartWords:
        myString.append(item)
        
    #used to get the last n items of the list
    n = nGramNumber - 1
    #holds on to the most likely word until appended to myString
    nextWord = ""                      
                         
    #we're making a sentence of length numberOfWords
    while len(myString) < numberOfWords:
        #creates a context from the previous n words 
        context = (myString[len(myString)-n:][0] + " " + myString[len(myString)-n:][1]) 
        
        #we'll compare probabilities to find the best fitting key to match the context                    
        max_probability = 0
        
        for item in distribution.items():
                
                #renamed to make it easier to understand. key is the word we're looking at, value is its context
                key = item[0][0]
                value = item[0][1]
                probability = item[1]
                
                if value == context:
                    if probability >= max_probability:               # perhaps randomizing > and >= would avoid patterns
                        #holds on to the new probability value in case another word is more likely
                        max_probability = probability
                        nextWord = str(key)
        
        print nextWord
        if (nextWord != '' and nextWord != myString[len(myString)-1:][0]):                
            myString.append(nextWord)
        else:
            
            randomStartWords = choice(distribution.keys())[1].split(" ") 
            
            print "reboot"
            #restart if it hits a null context
            if randomStartWords[0] == '' or randomStartWords[0] == myString[len(myString)-1:][0]:
                randomStartWords = choice(distribution.keys())[1].split(" ") 
                
            print "reboot2"
            
            myString.append(randomStartWords[0])
            
    return myString

print makeRandomTrigram(5)