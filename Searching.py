import torch
from transformers import BertTokenizer, BertModel, BertForMaskedLM
from sentence_transformers import *
import scipy.spatial
import pymongo

embedder = SentenceTransformer('bert-base-nli-mean-tokens')


class DataBaseInterface:
    def __init__(self):
        self.iDs = []
        self.corpus = []
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.database = self.myclient["Papers"]
        #collection
        self.collection = self.database["entries"]
        self.FillCorpus()

    def FillCorpus(self):
        for entry in self.collection.find():
            self.iDs.append(entry["_id"])
            self.corpus.append(entry["summary"])
            #print("Pushing back:\n      Id - " + str(entry["_id"]) + " \n      Summary - " + entry["summary"])
    # Frequency update of database
    def Update(self):
        pass
    # Takes in a project description and returns relevant corpus (lessons)
    # Sends top summaries to the screen
    # returns list of id's ordered by relevancy
    def SearchCorpus(self,inputQuery,closest_n=3):
        test_sentences = [inputQuery]
        corpus_embeddings = embedder.encode(self.corpus)
        query_embeddings = embedder.encode(test_sentences)

        topObjIds = []
        for query, query_embedding in zip(test_sentences, query_embeddings):
            distances = scipy.spatial.distance.cdist([query_embedding], corpus_embeddings, "cosine")[0]

            results = zip(range(len(distances)), distances)
            results = sorted(results, key=lambda x: x[1])

            print("\n\n======================\n\n")
            print("Query:", query)
            print("\nTop %s most similar sentences in corpus:\n" % closest_n)

            for idx, distance in results[0:closest_n]:
                index = self.corpus.index(self.corpus[idx])
                topObjIds.append(self.iDs[index])
                print(self.corpus[idx].strip(), "(Score: %.4f)" % (1-distance))
        return topObjIds

database = DataBaseInterface()
x = database.SearchCorpus("n Natural Language Processing (NLP), it is hard to predict ifsharing will lead to improvements, particularly if tasks are only looselyrelated. To overcome this, we introduce Sluice Networks")
print(x)