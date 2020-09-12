import pandas as pd
import json
import torch
import json 
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
import re
import pymongo
df = pd.read_excel('/home/rmslick/NasaHackathon/Data/LLDBExport_hackathon.xlsx')
model = T5ForConditionalGeneration.from_pretrained('t5-small')
tokenizer = T5Tokenizer.from_pretrained('t5-small')
device = torch.device('cpu')

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
#Single item intry
def InsertItem(dictionary):
    mydb = myclient["Lessons"]
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
                                        max_length=250,
                                        early_stopping=True)
    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return output
keys = df.columns
keys = list(keys)
keys.append('corpus')
#print(list(keys))
lessonsLearned = []
allColumns = []
for i in range(21):
    #obtain column data
    allColumns.append(df[keys[i]].tolist())

lessonsLearned = []
corpus = []
for i in range(0,2114):
    entry = []
    lessonSummary = ""
    for j in range(21):
        entry.append(allColumns[j][i])
        if keys[j] == 'Lesson':
            lesson = allColumns[j][i]
            try:
                lessonStripped = remove_html_tags(lesson)
            except:
                lessonStripped = lesson
            # Generate a corpus
            try:
                lessonSummary = Summarize(lessonStripped)
            except:
                lessonSummary = ""
    entry.append(lessonSummary)
    #add condition to generate corpus
    lessonDict = dict(zip(keys,entry))
    #print(lessonDict)
    lessonsLearned.append(lessonDict)
    print(str(i/2114) +" percent done.")
for i in lessonsLearned:
    InsertItem(i)
    
print("Database full!")