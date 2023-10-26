from fastapi import FastAPI
from transformers import pipeline
from better_profanity import profanity
import random
import json

classifier = pipeline("text2text-generation", model="Rozi05/QuoteVibes_Model_Trained")
profanity.load_censor_words()

with open("tags.json", "r") as file:
    tags_data = json.load(file)

app = FastAPI()

@app.get("/get-quote/{tag}")
async def get_quote(tag: str):
    tagsInUse = []
    for i in range(5):
        while True:
            chosen_tag = random.choice(tags_data["tags"])
            if (chosen_tag not in tagsInUse) and chosen_tag != tag:
                tagsInUse.append(chosen_tag)
                break

    if tag == "default":
        tags = f"{tagsInUse[0]};{tagsInUse[1]};{tagsInUse[2]};{tagsInUse[3]};{tagsInUse[4]}"
    else:
        tags = f"{tag};{tagsInUse[0]};{tagsInUse[1]};{tagsInUse[2]};{tagsInUse[3]};{tagsInUse[4]};{tag}"
        
    while True:
        models_quote = classifier(tags)

        check_for_profanity = profanity.censor(models_quote[0]["generated_text"])
        test_for_text = models_quote[0]["generated_text"].replace(" ", "x")
        
        if not ("*" in check_for_profanity) or test_for_text != "xxxxxxxxx":
            return {"quote": models_quote[0]["generated_text"]}
