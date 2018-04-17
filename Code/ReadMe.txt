Text Summarization
Created by Nicholas Buzzanca

Requires sklearn and nltk python libraries.

How to use:
1. Create a corpus containing all data in an array.  EX:
	corpus[0] = "This is document 1."
	corpus[1] = "This is document 2."
	...
2. Call getDictionary(corpus) using the corpus you created and store the result.

3. Call Summarize_Document(dictionary, corpus, document, threshold, mmr_threshold
			, isSmallSummary, maxLen)
	
	*dictionary is the result of step 2

	*corpus is the result of step 1

	*document is a single string which is the document to be summarized

	*threshold is a value from 0 to 1 which represents how similar sentences 
	 need to be in order to be grouped together.  a value of 1 would mean the
	 sentences need to be exactly the same, whereas a value of 0 would mean
	 all sentences would form a single giant group.

	*mmr_threshold is a value from 0 to 1 which represents how different sentences
	 need to be to be added to the summary.  A higher value means that sentences 
	 need to be more different to be added, whereas a lower value means that
	 sentences can be fairly similar to eachother and still be in the summary.

	*isSmallSummary is a boolean value.  Sending in True means that the program will
	 only consider the first sentence of each section.  Sending in False will mean
	 the program will consider each sentence individually but always consider the first
	 sentence of each section.
	
	*maxLen is a position integer.  This represents the maximum length the resulting
	 summary can be.

full example code:

	corp = [None] * 20

	for index in range(0,20):
    		with open('wiki' + str(index+1) + '.txt', 'r') as myfile:
        		corp[index] = myfile.read().replace('\n', ' ')


	doc = corp[19]
	dic = getDictionary(corp)
	Summarize_Document(dic,corp,doc,.3,.5, False, 6)