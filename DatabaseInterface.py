import json
import torch
import json 
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
import pymongo

model = T5ForConditionalGeneration.from_pretrained('t5-small')
tokenizer = T5Tokenizer.from_pretrained('t5-small')
device = torch.device('cpu')
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

#Single item intry
def InsertItem(dictionary):
    mydb = myclient["Papers"]
    #collection
    mycol = mydb["entries"]
    x = mycol.insert_one(dictionary)

def Summarize(body):
    t5_prepared_Text = "summarize: "+body
    tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors="pt").to(device)
    # summmarize 
    summary_ids = model.generate(tokenized_text,
                                        num_beams=4,
                                        no_repeat_ngram_size=2,
                                        min_length=30,
                                        max_length=200,
                                        early_stopping=True)
    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return output
# Load json file
#{location, title, author, summary ,fulltext} = search fields
def LoadDataJSON(filepath):
    f = open(filepath)
    # returns JSON object as  
    # a dictionary 
    data = json.load(f)
    for i in range(5):
        # Iterating through the json list
        author =  data[i]["author"]
        body = data[i]["summary"]
        body = body.replace('\n','')
        #Obtain summary
        summary = Summarize(body)
        #Build dictionary
        entry = {"_id":i+1,"author":author,"summary":summary,"fullBody":body}        
        InsertItem(entry)
    f.close()
dataPath = "Data/arxivData.json"
LoadDataJSON(dataPath)
myclient.close()
