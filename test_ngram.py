#=-= coding=utf-8 =-=
from Dictionary import Dictionary
from Ngram import Ngram


def printSeg(segMap,sentence):
    if(segMap.has_key(sentence)):
        pair = segMap[sentence]
        if(isinstance(pair,tuple)):
            printSeg(segMap,pair[0])
            printSeg(segMap,pair[1])
        else:
            if(sentence==pair):
                print sentence
            else:
                printSeg(segMap,pair)
    else:
        print sentence


#读入分词后的数据
#dict1 = Dictionary("./dict1.txt")
dict1 = Dictionary("./operationName_ZipfRanking.txt")


while(True):
    ngram1 =Ngram(dict1)
    #sentence = raw_input("please input a Chinese Sentence:").decode("utf-8");
    sentence = u'肝术'
    print ngram1.maxP(sentence)
    segmap=ngram1.getSeg()
    print ngram1.splitsentence("ABC")
    break
    
    #for eachkey in segmap:
               
     #   if(isinstance(segmap[eachkey],tuple)):
      #      print (eachkey+":"+segmap[eachkey][0]+','+segmap[eachkey][1])
       # else:
        #    print (eachkey+":"+segmap[eachkey])
    printSeg(segmap,sentence)
