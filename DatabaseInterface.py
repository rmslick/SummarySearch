import torch
from transformers import BertTokenizer, BertModel, BertForMaskedLM
from sentence_transformers import *
import scipy.spatial
import pymongo
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config

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
        #For summarization
        self.model = T5ForConditionalGeneration.from_pretrained('t5-small')
        self.tokenizer = T5Tokenizer.from_pretrained('t5-small')
        self.device = torch.device('cpu')
    #Called to synch instance with database
    def FillCorpus(self):
        for entry in self.collection.find():
            self.iDs.append(entry["_id"])
            self.corpus.append(entry["summary"])
            #print("Pushing back:\n      Id - " + str(entry["_id"]) + " \n      Summary - " + entry["summary"])
    
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
    def SearchCorpus(self,inputQuery,closest_n=3):
        test_sentences = [inputQuery]
        corpus_embeddings = embedder.encode(self.corpus)
        query_embeddings = embedder.encode(test_sentences)

        topObjIds = []
        # Corpus seearch
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
while True:
    choice = input("Enter an option 1-5\n1) Look up\n2) Smart Search: Enter a project description \n3) Add a lesson \n4) Risk Analysis \n5) NASA Problems \n6) Visualize")
    if choice == "1":
        pass
    elif choice == "2":
        description = input("Enter a project description")
        x = database.SearchCorpus(description)
        print(x)
    elif choice == "3":
        author = input("Enter an author")
        fullBody = input("Enter a full body")
        database.AddLesson(author,fullBody)
    print(x)