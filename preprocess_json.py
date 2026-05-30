import requests 
import os 
import json
import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 
import joblib


def create_embedding(all_text):
    print("thinking...")
    r = requests.post("http://localhost:11434/api/embed",json={
    "model":"bge-m3",
    "input":all_text
    })

    
    embedding = r.json()["embeddings"]
    return embedding

jsons = os.listdir("newjsons")
#print(jsons)

my_dict = []
chunk_id = 0

for json_file in jsons:
    print(f"Creating Embeddings for {json_file}")
    with open(f"newjsons/{json_file}") as f:
        content = json.load(f)
    all_texts = [c["text"] for c in content["chunks"]]
    embedding = create_embedding(all_texts)


    total = len(content["chunks"])

    for i,chunk in enumerate(content["chunks"]):   
        chunk["chunk_id"] = chunk_id
        chunk_id += 1  
        chunk["embedding"] = embedding[i]
        chunk["filename"] = json_file
        my_dict.append(chunk)

        #print(f"{i+1}/{total} - chunk_id:{chunk_id} chunks done ...")
        # print(f"text :{chunk['text']}")
        # print(chunk)
    # print(my_dict)


df = pd.DataFrame.from_records(my_dict)

joblib.dump(df,"embedding.joblib")
#save this dataframe 
print(len("embedding.joblib"))