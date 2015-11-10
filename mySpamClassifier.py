# Naive Bayes Classifer
# Create classifier with methods train, classify, and accuracy.
# Retrieve and label spam and ham documents from spam and ham directories.
# The features are the 2000 most common words in all the documents.
# Each feature gets a say in deciding which label should be assigned to a given input value.
# Starts by calculating prior probability of each label, determined by the frequency of
# each label in the training set, e.g. 60 spam and 40 ham out of 100 files, 
# spam has a 60% prior probability and ham has a 40% prior probability.
# Each feature contributes to the prior probability to get a likelihood estimate foe each label.
# The label with the highest likelihood estimate is assigned to the input value, 
# e.g. 39% estimate for spam, 61% estimate for ham, file is assigned "ham".
import nltk
import os
import random
import time
from nltk.corpus import stopwords
stopwords = nltk.corpus.stopwords.words('english') #all non-descriptive English words  
class mySpamClassifier:
        def __init__(self, spamFolder, hamFolder):
                self.totalSpamWords = []
                self.totalHamWords = []
                self.totalSpamFile = []
                self.spamFiles = os.listdir(spamFolder)
                self.totalHamFile = []
                self.hamFiles = os.listdir(hamFolder)
                self.spam_prob = {}
                self.ham_prob = {}

                # message
                print("Begin parsing files...")
                start = time.process_time()
                
                for docs in self.spamFiles:
                        textFile = open(spamFolder + "/" + docs, "r", encoding='ISO-8859-1')
                        lines = textFile.readlines()
                        textFile.close()
                        wordList = [w.split() for w in lines]#splits the lines into words
                        words = sum(wordList, [])#flattens inot a simple list of all words
                        featureWords = [w.lower() for w in words if w not in stopwords and len(w) > 1 and w.isalpha()] #omits needless words
                        featureWords = list(set(featureWords))  # remove duplicates
                        self.totalSpamFile.append((featureWords, "spam")) # assigns label for file
                        self.totalSpamWords += featureWords #adds words to total words
                        
                for docs in self.hamFiles:
                        textFile = open(hamFolder + "/" + docs, "r", encoding='ISO-8859-1')
                        lines = textFile.readlines()
                        textFile.close()
                        wordList = [w.split() for w in lines]#splits the lines into words
                        words = sum(wordList, [])#flattens inot a simple list of all words
                        featureWords = [w.lower() for w in words if w not in stopwords and len(w) > 1 and w.isalpha()] #omits needless words
                        featureWords = list(set(featureWords))  # remove duplicates
                        self.totalHamFile.append((featureWords, "ham")) # assigns label for file
                        self.totalHamWords += featureWords #adds words to total words
                        
                self.documents = self.totalSpamFile
                self.documents += self.totalHamFile
                random.shuffle(self.documents)#list with spam and ham documents randomly distributed

                certainIndex = int(len(self.documents)*0.9)#getting 90% and 10% of the total documents
                self.trainDocs = self.documents[:certainIndex] #90% of total documents
                self.testDocs = self.documents[certainIndex:] #10% of total documents
                self.totalWords = self.totalSpamWords + self.totalHamWords 
                random.shuffle(self.totalWords)
                self.all_words = nltk.FreqDist(w for w in self.totalWords if w.isalpha())#lists frequency of all words
                self.word_features = list(self.all_words)[:2000] #lists top 2000 most frequent words

                elapsed = time.process_time() - start
                print("Parsing done in %6.4f seconds!\n" % elapsed)
                

        def train(self): #trains the classifier by calculating probabilities
                self.total_spam_docs = 0
                self.total_ham_docs = 0

                # message
                print("Begin training...")
                start = time.process_time()
                
                # prob of doc being spam
                for doc in self.trainDocs:
                        if doc[1] == "spam":
                                self.total_spam_docs += 1
                        else:
                                self.total_ham_docs += 1
                self.s_prob = float(self.total_spam_docs) / len(self.trainDocs)
                self.h_prob = float(self.total_ham_docs) / len(self.trainDocs)
                print("Probability doc is spam: %4.2f%%: " % (self.s_prob * 100))
                print("Probability doc is ham: %4.2f%%: " % (self.h_prob * 100))

                # prob of word being spam 
                eps = 1 / (len(self.trainDocs) + 1)
                for fword in self.word_features:
                        s_count = eps
                        h_count = eps
                        # default word prob to eps
                        self.spam_prob.setdefault(fword, eps)
                        self.ham_prob.setdefault(fword, eps)
                        # count words in spam and ham
                        for doc in self.trainDocs:
                                if fword in doc[0]:
                                        if doc[1] == "spam":
                                                s_count += 1
                                        else:
                                                h_count += 1
                        # set probability if not zero
                        if s_count != 0:
                                self.spam_prob[fword] = float(s_count) / self.total_spam_docs
                        if h_count != 0:
                                self.ham_prob[fword] = float(h_count) / self.total_ham_docs

                #print(self.spam_prob)
                elapsed = time.process_time() - start
                print("Training done in %6.4f seconds!\n" % elapsed)

                                
        def classify (self): #labels test docs as spam or ham based on feature probs.
                self.classifiedList = [] #list where docs are labeled

                print("Begin classification...")
                start = time.process_time()
                
                # for all the documents
                for doc in self.testDocs:
                        # multiply the prob of the doc and each spam/ham word
                        total_s_prob = self.s_prob
                        total_h_prob = self.h_prob
                        for word in doc[0]:
                                if word in self.word_features:
                                        total_s_prob *= self.spam_prob[word]
                                        total_h_prob *= self.ham_prob[word]
                        if total_s_prob > total_h_prob:
                                self.classifiedList.append((doc[0], "spam"))
                        else:
                                self.classifiedList.append((doc[0], "ham"))

                elapsed = time.process_time() - start
                print("Classification done in %6.4f seconds!\n" % elapsed)

                return self.classifiedList

        def accuracy (self): #calculates percent of docs that were correctly classified
                result = 0

                # count docs classified correctly
                i = 0
                for doc in self.testDocs:
                        if self.classifiedList[i][1] == doc[1]:
                                result += 1
                        i += 1

                # divide by total
                result /= len(self.testDocs)
                
                return result

if __name__ == '__main__':
        c = mySpamClassifier("spam", "ham")
        c.train()
        c.classify()
        accuracy = c.accuracy() * 100
        print("Documents correctly classified: %4.2f%%" % accuracy)
