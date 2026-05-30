import pandas as pd 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import requests

def create_embedding(all_text):
    r = requests.post("http://localhost:11434/api/embed",json={
    "model":"bge-m3",
    "input":all_text
    })

        
    embedding = r.json()["embeddings"]
    return embedding

def interface(prompt):
    r = requests.post("http://localhost:11434/api/generate",json={
    # "model":"deepseek-r1",
    "model":"llama3.2",
    "prompt":prompt,
    "stream" : False
    })

    response = r.json()
    print(response)

    return response

def infereance_openai():
    
    df= joblib.load("embedding.joblib") 

    df.to_parquet("embeddings.parquet")  #save embeddings 
    df = pd.read_parquet("embeddings.parquet") #read embeddings 

    pd.set_option('display.max_columns', None)  # show all columns
    pd.set_option('display.max_rows', 10)       # show 10 rows
    pd.set_option('display.width', None) 
    pd.set_option('display.max_colwidth', 30)  # limits embedding column width 

    #print(df)

    #now i want to ask a  query quesetion
    incoming_query = input("ask a question :")
    query_embedding = create_embedding([incoming_query])[0]
    # print("Query embedding done!")

    #find similarities of question embeddings with other embeddings 

    similarities = cosine_similarity(np.vstack(df["embedding"]),[query_embedding]).flatten()
    print(similarities)

    top_indices = np.argsort(similarities)[::-1][:5]

    for i in top_indices:
    print(f"Score: {similarities[i]:.4f}")
    print(f"Video Number: {df.iloc[i]['number']}")
    print(f"Title: {df.iloc[i]['title']}")
    print(f"Chunk ID: {df.iloc[i]['chunk_id']}")
    print(f"Start: {df.iloc[i]['start']}")
    print(f"End: {df.iloc[i]['end']}")
    print(f"Text: {df.iloc[i]['text']}")
    print("-" * 50)
    
    new_df = df.iloc[top_indices]   
    # print(new_df[["number","title","chunk_id","start","end","text"]])

    prompt = f'''I am teaching web development in my sigma web development cource. Here are viedeo subtitle  chunks containing video title,video number,start time in seconds,end time in seconds , the text at that time.
    {new_df[["title","number","start","end","text"]].to_json(orient="records")}

    ----------------------------

    "{incoming_query}"
    user asked the question related to the video chunks , you have to answer in a human way (don't mention the above formate it's just for you ) where and how much content is taught in which video  (in video and at what timestamp) and guide the user to go to that perticuler video . if user asks unrelated questions, that you can only answers realted to the cource  
    '''

    return prompt

prompt = infereance_openai()

with open ("prompt.txt","w")as f:
    f.write(prompt)

# response = (interface(prompt))["response"]
# print(response)

response = interface(prompt)["response"]
print(response)

with open ("response.txt","w")as f:
    f.write(response)

    # for index,item in new_df.iterrows():
        # print(index,item["title"],item["number"],item["text"],item["start"],item["end"])
