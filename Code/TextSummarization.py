from nltk.corpus import stopwords

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
import nltk


stopWords = stopwords.words('english')
count_vect = CountVectorizer()
symbol = ["~","`","!","@","#","$","%","^","&","*","(",")","_","-","+","=","{","}","[","]",":",">",";","'",",","<","/","?","*","-","+","\"","–","°","—"]


def invalidWord(word):#or word in stopWords
    for char in word:
        if len(word) == 1 or char.isdigit() or char in symbol:
            return True

    return False

def findInDic(dic, word):
    for index in range(0, len(dic)):
        if (dic[index][0] == word):
            return index
    return -1

# input: corpus...output: dictionary, df values
def getDictionary(corp):
    words = []
    #make dictionary
    for index in range(0,len(corp)):
        #break doc up into array of words
        doc = nltk.word_tokenize(corp[index])
        inner = len(doc)
        for index2 in range(0,inner):
            found = False
            for wordsIndex in range(0,len(words)):
                if doc[index2].lower() == words[wordsIndex][0]:
                    #increase df
                    words[wordsIndex][1] += 1
                    found = True
                    break
            if(not found):
                if (not invalidWord(doc[index2].lower())):
                    words.append([doc[index2].lower(), 1])
    return words

#dic is output of "getDictionary(corpus)", doc is a string, threshhold for grouping sentences,
#mmr_threshold for finding redundant sentences, mode is a bool that varies the output
def Summarize_Document(dic, corpus, doc, threshold, mmr_threshold, isSmallSummary, maxLen):
    #compute tfidfs of all words in doc
    corpus.append(doc)
    counts = count_vect.fit_transform(corpus)
    del corpus[len(corpus)-1]
    tfidf_transformer = TfidfTransformer()
    tfidf = tfidf_transformer.fit_transform(counts)
    features = count_vect.get_feature_names()


    scoreList = [None] * (len(corpus)+1)
    wordList = [None] * (len(corpus)+1)
    doc_id = 0
    for docu in tfidf.todense():
        word_id = 0
        wordListT = []
        scoreListT = []
        for score in docu.tolist()[0]:
            if score > 0:
                word = features[word_id]
                if not invalidWord(word):
                    scoreListT.append(score)
                    wordListT.append(word.lower())
            word_id += 1
        wordList[doc_id] = wordListT
        scoreList[doc_id] = scoreListT
        doc_id += 1

    #cosine similarity::
    #for each sent
    sent = doc.split('.')
    if(len(sent[len(sent)-1]) == 0):
        del sent[len(sent)-1]
    sentences = [None] * len(sent)
    #for s in sent:
    for index in range(0, len(sent)):
        sentWords = sent[index].split(' ')
        # now we have the words per ea sentence per ea doc...
        sentTFIDF = [0] * len(dic)
        # for each word
        for index2 in range(0, len(sentWords)):
            if findInDic(dic,sentWords[index2].lower()) != -1:
                #i = index of word in dictionary
                i = findInDic(dic,sentWords[index2].lower())
                #j = tfidf value key
                j = wordList[len(wordList)-1].index(sentWords[index2].lower())
                sentTFIDF[i] = scoreList[len(scoreList)-1][j]
        sentences[index] = sentTFIDF
    cosine_sim = [0] * (len(sentences)-1)
    for index in range(0, len(sentences) - 1):
        cosine_sim[index] = cosine_similarity(sentences[index], sentences[index + 1])
    out = []
    out.append(sent[0] + ".\n")
    outtf = []
    outtf.append(sentences[0])
    Len = len(cosine_sim)
    secLen = int(maxLen /3)
    thisSec = Len /3
    secLen -= 1
    if isSmallSummary:
        count = 1
        for index in range(0,Len):
            if (secLen != 0):
                if cosine_sim[index] < threshold:
                    cos_compare = []
                    for i in range(0,len(outtf)):
                        cos_compare.append(cosine_similarity(outtf[i],sentences[index+1]) < mmr_threshold)
                    if all(cos_compare):
                        if(len(sent[index+1].split(' ')) < 3):
                            pass#do nothing
                        else:
                            secLen -= 1
                            outtf.append((sentences[index+1]))
                            out.append(sent[index+1] + ".\n")
                    count = 0
                count += 1
            if index > thisSec:
                thisSec *= 2
                secLen = int(maxLen / 3)

    outsec = [sentences[0]]
    if not isSmallSummary:
        count = 1
        for index in range(0, len(cosine_sim)):
            if (secLen != 0):
                if cosine_sim[index] < threshold:

                    if (len((sent[index + 1]).split(' ')) < 3):
                        pass#do nothing
                    else:
                    #always add first sent of each section
                        outtf.append(sentences[index + 1])
                        outsec = []
                        outsec.append(sentences[index + 1])
                        secLen -= 1
                        out.append(sent[index + 1] + ".\n")
                        count = 0
                else:
                    cos_compare = []
                    for i in range(0,len(outsec)):
                        cos_compare.append(cosine_similarity(outsec[i], sentences[index + 1]) < mmr_threshold)
                    if all(cos_compare):
                        if (len((sent[index + 1]).split(' ')) < 3):
                            pass#do nothing
                        else:
                            outtf.append((sentences[index + 1]))
                            outsec.append(sentences[index + 1])
                            secLen -= 1
                            out.append(sent[index + 1] + ".\n")
                count += 1
            if index > thisSec:
                thisSec *= 2
                secLen = int(maxLen / 3)


    with open("output.txt","w") as file:
        for sent in out:
            file.write(sent)
        file.close()
#main:

