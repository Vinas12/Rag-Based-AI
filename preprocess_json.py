import requests #is a python tool used to send the http requests using python
import os 
import json
import pandas as pd 
import joblib


def create_embedding(texts):
    print("thinking...")
    r = requests.post("http://localhost:11434/api/embed",json={  #send the post request to your local ollama server,/api/embed endpoint takes a model name and some input text, and returns vector embeddings for that text. 
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
    texts = [c["text"] for c in content["chunks"]]
    embedding = create_embedding(texts)


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


df = pd.DataFrame.from_records(my_dict)#create a dataframe

joblib.dump(df,"embedding.joblib")#save this dataframe 

print(len("embedding.joblib"))
