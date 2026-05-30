import whisper
import json
import os

audios = os.listdir("audios")

for audio in audios:
    if("_"in audio):
        numbers = audio.split(" ")[0]
        title = audio.split(" ")[1][:-4]
        print(numbers,title)

        model = whisper.load_model("large-v2")

        result = model.transcribe(f"audios/{audio}",
        #result = model.transcribe(f"audios/sample.mp3",
                                    language = "hi",
                                    task="translate",
                                    word_timestamps=False)

        chunks = []
        for segment in result["segments"]:
            chunks.append({"number":numbers,"title":title,"start":segment["start"],"end":segment["end"],"text":segment["text"]})

        chunks_with_matadata = {"chunks":chunks , 
                                "text": result["text"]
        }

        with open (f"jsons/{audio}.json","w")as f :
            json.dump(chunks_with_matadata,f,indent=4)

