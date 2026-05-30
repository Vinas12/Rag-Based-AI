import os
import math
import json 

n = 5

for filename in os.listdir("jsons"):
    if filename.endswith(".json"):
        file_path = os.path.join("jsons",filename)
        with open(file_path,"r",encoding="utf-8")as f :
            data = json.load(f)
            new_chunk =[]
            num_chunk = len(data["chunks"])
            num_groups = math.ceil(num_chunk/n)

            for i in range(num_groups):
                start_idx = i*n
                end_idx = min((i+1)*n, num_chunk)

                chunk_group = data["chunks"][start_idx: end_idx]

                new_chunk.append({
                    "number" : data["chunks"][0]["number"],
                    "title" : chunk_group[0]["title"],
                    "start" : chunk_group[0]["start"],
                    "end" : chunk_group[-1]["end"],
                    "text": " ".join([c["text"] for c in chunk_group])
                })

                #save fil without double .json

                os.makedirs("newjsons",exist_ok=True)
                with open(os.path.join("newjsons",filename),"w",encoding="utf-8")as json_file:
                    json.dump({"chunks":new_chunk,"text": data["text"]},json_file,indent=4)


