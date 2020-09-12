import torch
from transformers import BertTokenizer, BertModel, BertForMaskedLM
from sentence_transformers import *
import scipy.spatial
import pymongo
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
import json
import matplotlib.pyplot as plt
embedder = SentenceTransformer('bert-base-nli-mean-tokens')


class DataBaseInterface:
    def __init__(self):
        self.iDs = []
        self.corpus = []
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.database = self.myclient["Lessons"]
        #collection
        self.collection = self.database["entries"]
        self.groupCollection = self.database["groups"]

        self.dataFull = self.collection.find()
        self.titles = []
        self.groups = []
        self.FillCorpusAndTitles()
        #For summarization
        self.model = T5ForConditionalGeneration.from_pretrained('t5-small')
        self.tokenizer = T5Tokenizer.from_pretrained('t5-small')
        self.device = torch.device('cpu')
        self.corpusTitleDict = {}
    #Called to synch instance with database
    def FillCorpusAndTitles(self):
        for entry in self.dataFull:
            #self.iDs.append(entry["_id"])
            self.corpus.append(entry['corpus'])
            self.titles.append(str(entry['Title']))
    #Filed based search returns all matches that satisfy json criteria
    #Format must be "key":"" in empty field case or "key":"value"
    
    #Returns a list of all matches that equal criteria
    #Need test case
    # Add sentiment or set fields in ui directly
    def BasicSearch(self, entryDict):
        lessonsFound = []
        for entry in self.dataFull:
            #if every entry in maps
            found = 1
            for key in entryDict:
                if entryDict[key] != "":
                    #Check for mismatch in case
                    if entryDict[key] != entry[key]:
                        found = 0
                        break
            if found == 1:
                lessonsFound.append(entry)
        return lessonsFound
    # SummarizeDB
    def SummarizeEntry(self, fullBody):
        t5PreparedText = "summarize: "+ fullBody
        tokenizedText =  self.tokenizer.encode(t5PreparedText, return_tensors="pt").to(self.device)
        summaryIds = self.model.generate(tokenizedText,
                                        num_beams=4,
                                        no_repeat_ngram_size=2,
                                        min_length=30,
                                        max_length=200,
                                        early_stopping=True)
        summary = self.tokenizer.decode(summaryIds[0], skip_special_tokens=True)
        return summary
    def AddLesson(self, author, fullBody):
        _id = len(self.corpus) + 1
        summary = self.SummarizeEntry(fullBody)
        self.corpus.append(summary) #update corpus
        dictionary = {"_id":_id, "author":author,"summary":summary,"fullBody":fullBody}
        self.collection.insert_one(dictionary) #Fill DB
    def RiskAnalysis(self, projectSummary):
        summaries = [projectSummary]
        indexes = Similarity(summaries,self.corpus)
    def SmartSearchCorpus(self,inputQuery):
        closest_n = 5
        test_sentences = [inputQuery]
        corpus_embeddings = embedder.encode(self.corpus)
        query_embeddings = embedder.encode(test_sentences)

        topObjIds = []
        # Corpus search
        for query, query_embedding in zip(test_sentences, query_embeddings):
            distances = scipy.spatial.distance.cdist([query_embedding], corpus_embeddings, "cosine")[0]

            results = zip(range(len(distances)), distances)
            results = sorted(results, key=lambda x: x[1])

            print("\n\n======================\n\n")
            print("Query:", query)
            print("\nTop %s lessons learned in corpus:\n" % closest_n)

            for idx, distance in results[0:closest_n]:
                index = self.corpus.index(self.corpus[idx])
                topObjIds.append(self.titles[index])
                print(self.titles[idx].strip(), "(Score: %.4f)" % (1-distance))
        return topObjIds
    
    def Graph(self,inputQuery):
        closest_n = 25
        test_sentences = [inputQuery]
        corpus_embeddings = embedder.encode(self.corpus)
        query_embeddings = embedder.encode(test_sentences)

        topObjIds = []
        # Corpus search
        scores = []
        x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
        for query, query_embedding in zip(test_sentences, query_embeddings):
            distances = scipy.spatial.distance.cdist([query_embedding], corpus_embeddings, "cosine")[0]

            results = zip(range(len(distances)), distances)
            results = sorted(results, key=lambda x: x[1])

            print("\n\n======================\n\n")
            print("Query:", query)
            print("\nTop %s lessons learned in corpus:\n" % closest_n)

            for idx, distance in results[0:closest_n]:
                index = self.corpus.index(self.corpus[idx])
                topObjIds.append(self.titles[index])
                scores.append((1-distance)*100)
        range1 = (0, 25) 
        plt.hist(scores,25,range1,color="green",histtype = 'bar', rwidth = 0.8)
        plt.show() 
    #return a list of indexes satisfying the rVal
    def Similarity(self, test_sentences, lst_corpus):
        global embedder
        corpus_embeddings = embedder.encode(lst_corpus)
        query_embeddings = embedder.encode(test_sentences)
        closest_n = len(lst_corpus)
        for query, query_embedding in zip(test_sentences, query_embeddings):
            distances = scipy.spatial.distance.cdist([query_embedding], corpus_embeddings, "cosine")[0]

            results = zip(range(len(distances)), distances)
            results = sorted(results, key=lambda x: x[1])

            #print("\n\n======================\n\n")
            #print("Query:", query)
            #print("\nTop %s most similar sentences in corpus:\n" % closest_n)
            indexes = []
            count = 0
            for idx, distance in results[0:closest_n]:
                #print(lst_corpus[idx].strip(), "(Score: %.4f)" % (1-distance))
                score = (1-distance)
                if score > 0.65:
                    #print(lst_corpus[idx].strip(), "(Score: %.4f)" % (1-distance))
                    #print(idx)
                    indexes.append(idx)
        return indexes

    #Take in a title-> Output all titles greater than 50 and maps
    def BuildProfile(self, title):
        #rval is all titles of other lessons similar at the thresh > 65
        titles = [titles]
        rVal = Similarity(titles, self.titles)
    def GroupingAlgorithm(self):
        lengthW = len(self.corpus[1:])
        length = 1
        testSentence = []
        testSentence.append(self.corpus[1]) # Initial Query
        testCorpus = self.corpus[1:] # Initial corpus
        testTitles = self.titles[1:]
        while length != 0:
            try:
                #obtian all indexes of similarity with rval > 55
                indexes = database.Similarity(testSentence,testCorpus)

                groupCorpus = []
                groupTitle = []
                #use indices to trim the corpus and create a new group element
                counter = 0
                counters = []
                for i in indexes:
                    #print("Index attempt: " + str(i))
                    groupCorpus.append(testCorpus[i])
                    groupTitle.append(testTitles[i])
                    counters.append(str(counter))
                    counter += 1
                newCorpus = []
                newTitle = []

                for i in range (len(testCorpus)):
                    #if not in indexes then ad
                    if i not in indexes:
                        newCorpus.append(testCorpus[i])
                        newTitle.append(testTitles[i])
                testCorpus = newCorpus 
                testTitles = newTitle
                #Create a dictionary to represent group
                group = dict(zip(counters,groupTitle))
                #Append dictionary
                self.groups.append(group)
                #update length for while loop check
                length = len(testCorpus)
                #Next element in line
                testSentence = [testCorpus[0]]
                #sanity is not overrated
                self.groupCollection.insert_one(group)
                print("Group added to database and "+str(1-length/lengthW)+" percent done")        
            except:
                break
database = DataBaseInterface()