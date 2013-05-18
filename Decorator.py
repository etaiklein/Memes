import ast

#Creates a list describing the various features of a meme.

# the following are characteristics of the image

# 1 if human, 0 if animal
# 1 if can be determined to be male
# 1 if can be determined to be female
# 1 if archetype
# 1 if color wheel
# 1 if full photo, 2 if photo vignette
# 1 if drawn, 2 if Rage Comic
# 1 if bait and switch
# 1 if antihumor
# 1 if evil, 2 if good
# 0 if baby, 1 if adult, 2 if old

# the following pertains to content which can't be easily coded:
# 1 if pop character or reference, 0 if original character
# 1 if it contains drug references

#the following pertains to content of the meme which has to be coded

# average word length                                        done
# similarity of the first 3 words of each meme
# probability score of being a common english sentence

# number of cursewords                                        done
# count of text on top vs. text on bottom.                    done
# count the total length of the string                        done

# of third person words                                      done
# of first person words                                      done
# of second person words                                     done

# adds a dictionary of counts (features) to each title
def decorateTitles():
    with open("Sample.txt", "r") as g:
        with open("SampleDecorated.txt", "a") as t:
            titles = g.readlines()

            for title in titles:
                if title[0] == "/":
                    adict = decorateOneTitle(title)
                    t.write(title.strip("\n") + " *dict* " + str(adict) + "\n")

#computes various counts for a single title.
def decorateOneTitle(title):
    mydict = {}
    mystring = title.split(" - ")[1]
    top, bottom = splitThis(mystring)
    
    mydict["wordCount"] = countWords(top,bottom)
    mydict["letterRatio"] = countLettersPerWord(mystring)
    mydict["countRatio"] = countRatio(top, bottom)
    mydict["thirdPersonWords"] = countThirdPerson(mystring)
    mydict["secondPersonWords"] = countSecondPerson(mystring)
    mydict["firstPersonWords"] = countFirstPerson(mystring)
    mydict["curseCount"] = getCurses(mystring)
    
    return mydict
    
#splits a string into its top and bottom
def splitThis(string):
    mylist = string.split("*^* ")
    top = mylist[0].strip().split(" ")
    bottom = mylist[len(mylist) - 1].strip().split(" ")
    return (top,bottom)

#adds two strings
def countWords(top, bottom):
    return len(top) + len(bottom)

#counts number of letters per word
def countLettersPerWord(string):
    mylist = string.strip("*^* ").split(" ")
    mycount = 0
    for word in mylist:
        for character in word:
            mycount += 1
    return mycount / float(len(mylist))
 

#counts the ratio of words in two strings
def countRatio(top, bottom):
    return float(len(top)) / float(len(bottom))
    
#determines number of third person present words in a string
def countThirdPerson(string):
    with open("thirdPerson.txt", "r") as f:
        mylist = string.strip("*^* ").split(" ")
        return len([val for val in mylist if val in f.readlines()])

#determines number of first person in a string.
def countFirstPerson(string):
    with open("firstPerson.txt", "r") as f:
        mylist = string.strip("*^* ").split(" ")
        return len([val for val in mylist if val in f.readlines()])

#determines number of firstperson in a string.
def countSecondPerson(string):
    with open("secondPerson.txt", "r") as f:
        mylist = string.strip("*^* ").split(" ")
        return len([val for val in mylist if val in f.readlines()])

#determines number of swearwords in a string
def getCurses(string):
    with open("swearWords.txt", "r") as f:
        mylist = string.strip("*^* ").split(" ")
        return len([val for val in mylist if val in f.readlines()])

#for all titles of each type, average their decorated scores
def decorateTypes():
    with open("SampleTypes.txt", "r") as f:
        with open("SampleDecorated.txt", "r") as t:
            with open("SampleTypesDecorated.txt", "a") as g:
                
                
                types = f.readlines()
                titles = t.readlines()
                i = 0
                
                for type in types:
                    
                    mydict = {}
                    
                    wordCount = 0
                    letterRatio = 0
                    countRatio = 0
                    thirdPersonWords = 0
                    secondPersonWords = 0
                    firstPersonWords = 0
                    curseCount = 0
                    titleCount = 0.0
                                        
                    while (titles[i].split(" - ")[0] == type.strip() and i < len(titles)-1):
                        newdict = ast.literal_eval(titles[i].split(" *dict* ")[1])
                        
                        wordCount += newdict["wordCount"]
                        letterRatio += newdict["letterRatio"]
                        countRatio += newdict["countRatio"]
                        thirdPersonWords += newdict["thirdPersonWords"]
                        secondPersonWords += newdict["secondPersonWords"]
                        firstPersonWords += newdict["firstPersonWords"]
                        curseCount += newdict["curseCount"]
                        titleCount += 1
                        
                        i+= 1
                    
                    if titleCount == 0:
                        titleCount += 1
      
                    mydict["wordCount"] = wordCount/titleCount
                    mydict["letterRatio"] = letterRatio/titleCount
                    mydict["countRatio"] = countRatio/titleCount
                    mydict["thirdPersonWords"] = thirdPersonWords/titleCount
                    mydict["secondPersonWords"] = secondPersonWords/titleCount
                    mydict["firstPersonWords"] = firstPersonWords/titleCount
                    mydict["curseCount"] = curseCount/titleCount
                    mydict["titleCount"] = titleCount
                    
                    g.write(type.strip() + " *dict* " + str(mydict) + "\n")

#for all titles of each type, give each visual scores by hand
def handDecorate():
    with open("MemeTypesDecorated.txt", "r") as f:
        with open("MemeTypesFinal.txt", "a") as g:
            types = f.readlines()
            i = 81
            while i < len(types)-1:
                type = types[i]
                newdict = ast.literal_eval(type.split(" *dict* ")[1])
                
                #the following format makes it easier to input 
                human = 0
                gendered = 0
                archetype = 0
                colorwheel = 0
                drawn = 0
                photo = 0
                aligned = 0
                aged = 0
                baitswitch = 0
                drugs = 0
                pop = 0
                
                print type.split(" *dict* ")[0].strip()
                
                features = raw_input("enter features here")
                features = features.split(", ")
                
                if "h" in features:
                    human = 1
                
                if "g" in features:
                    gendered = 1
                
                if "ar" in features:
                    archetype = 1
                
                if "c" in features:
                    colorwheel = 1
                
                if "d" in features:
                    drawn = 1
                
                if "r" in features:
                    drawn = 2
                
                if "ph" in features:
                    photo = 1
                
                if "v" in features:
                    vignette = 2
                
                if "ag" in features:
                    aged = 1
                
                if "al" in features:
                    aligned = 1
                
                if "dg" in features:
                    drugs = 1
                    
                if "b" in features:
                    baitswitch = 1
                
                if "po" in features:
                    pop = 1
                    
                if "q" in features or i == 100:
                    return
                    
                newdict["human"] = human
                newdict["gendered"] = gendered
                newdict["archetype"] = archetype
                newdict["colorwheel"] = colorwheel
                newdict["photo"] = photo
                newdict["drawn"] = drawn
                newdict["baitswitch"] = baitswitch
                newdict["aligned"] = aligned
                newdict["aged"] = aged
                newdict["drugs"] = drugs
                newdict["pop"] = pop

                g.write(type.split(" *dict* ")[0].strip() + " *dict* " + str(newdict) + "\n")
                
                i+=1
        