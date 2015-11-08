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
                self.spam_dict = {}
                self.ham_dict = {}
                
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


        def train(self): #trains the classifier by calculating probabilities
                self.total_spam_docs = 0
                self.total_ham_docs = 0
                for doc in self.trainDocs:
                        if doc[1] == "spam":
                                self.total_spam_docs += 1
                        else:
                                self.total_ham_docs += 1
                self.s_prob = float(self.total_spam_docs) / len(self.trainDocs)
                self.h_prob = float(self.total_ham_docs) / len(self.trainDocs)
                print("Spam Probability: %s: " % s_prob)
                print("Ham Probability: %s: " % h_prob)

                print("Word count: %s" % len(self.word_features))

                s_count = 0
                h_count = 0
                epsilon = 1 / (len(self.trainDocs) - 1)
                for fword in self.word_features:
                        self.spam_dict.setdefault(fword, epsilon)
                        self.ham_dict.setdefault(fword, epsilon)
                        for doc in self.trainDocs:
                                if fword in doc[0]:
                                        if doc[1] == "spam":
                                                s_count += 1
                                                self.spam_dict[fword] += 1
                                        else:
                                                h_count += 1
                                                self.ham_dict[fword] += 1
                        self.prob_s_word = spam_dict[fword] / s_count
                        self.prob_h_word = ham_dict[fword] / h_count
                        print(self.prob_s_word)
                        print(self.prob_h_word)
                                
        def classify (self): #labels test docs as spam or ham based on feature probs.
                self.classifiedList = [] #list where docs are labeled
                self.pro

                # for doc in self.trainDocs:
                #         for fword in word_features:
                                
                #                 if fword in doc:
                #                         word_s_prob = self.prob_s_word[fword] / self.prob_s_word.len
                #                         word_h_prob = self.prob_h_word[fword] / self.prob_h_word.len

                                
                                        
                #         if word_s_prob > word_h_prob:
                #                 self.classifiedList.append((doc, "spam"))
                #         else:
                #                 self.classifiedList.append((doc, "ham"))
                
                return self.classifiedList

        def accuracy (self): #calculates percent of docs that were correctly classified
                result = 0

                for 
                
                return result

if __name__ == '__main__':
        c = mySpamClassifier("spam", "ham")
        c.train()
        print("You don't want spam 'cause it's not ham.")
