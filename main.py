from fastapi import FastAPI

from transformers import pipeline
from better_profanity import profanity
import random
import json

app = FastAPI()

TAGS_PATH = "tags.json"
with open(TAGS_PATH, "r") as file:
    TAGS_DATA = json.load(file)

print(random.choice(TAGS_DATA["tags"]))

classifier = pipeline("text2text-generation", model="Rozi05/QuoteVibes_Model_Trained")

@app.get("/")
async def root():
    return {"message": "Go to get-quote to generate a quote with a tag."}

@app.get("/get-quote/{tag}")
async def get_quote(tag: str):
    for i in range(5):
        if i == 0:
            tag_1 = random.choice(TAGS_DATA["tags"])
            while tag_1 == tag:
                tag_2 = random.choice(TAGS_DATA["tags"])
            
        if i == 1:
            tag_2 = random.choice(TAGS_DATA["tags"])
            while tag_2 == tag_1 or tag_2 == tag:
                tag_2 = random.choice(TAGS_DATA["tags"])
                
        elif i == 2:
            tag_3 = random.choice(TAGS_DATA["tags"])
            while tag_3 == tag_1 and tag_3 == tag_2 or tag_3 == tag:
                tag_3 = random.choice(TAGS_DATA["tags"])
        
        elif i == 3:
            tag_4 = random.choice(TAGS_DATA["tags"])
            while tag_4 == tag_1 and tag_4 == tag_2 and tag_4 == tag_3 or tag_4 == tag:
                tag_4 = random.choice(TAGS_DATA["tags"])
        
        elif i == 4:
            tag_5 = random.choice(TAGS_DATA["tags"])
            while tag_5 == tag_1 and tag_5 == tag_2 and tag_5 == tag_3 and tag_5 == tag_4 or tag_5 == tag:
                tag_5 = random.choice(TAGS_DATA["tags"])

    if tag == "default":
        tags = f"{tag_1};{tag_2};{tag_3};{tag_4};{tag_5}"
    else:
        tags = f"{tag};{tag_1};{tag_2};{tag_3};{tag_4};{tag_5};{tag}"

    models_quote = classifier(tags)
    profanity.load_censor_words()

    check_for_profanity = profanity.censor(models_quote[0]["generated_text"])
    test_for_text = models_quote[0]["generated_text"].replace(" ", "x")

    while "*" in check_for_profanity or test_for_text == "xxxxxxxxx":
        models_quote = classifier(tags)

        check_for_profanity = profanity.censor(models_quote[0]["generated_text"])
        test_for_text = models_quote[0]["generated_text"].replace(" ", "x")

    return {"quote": models_quote[0]["generated_text"]}
