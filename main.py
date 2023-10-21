from fastapi import FastAPI
from transformers import pipeline
from better_profanity import profanity
import random
import json

app = FastAPI()

tags_file_path = "tags.json"
with open(tags_file_path, "r") as file:
    tags_data = json.load(file)

profanity.load_censor_words()

model_name = "Rozi05/QuoteVibes_Model_Trained"
classifier = pipeline("text2text-generation", model=model_name)

@app.get("/")
async def root():
    return {"message": "Make sure your url is for the right page."}

@app.get("/get-quote/{tag}")
async def get_quote(tag: str):
    tagsInUse = []
    for _ in range(5):
        while True:
            chosen_tag = random.choice(tags_data["tags"])
            if (chosen_tag not in tagsInUse) and chosen_tag != tag:
                tagsInUse.append(chosen_tag)
                break

    if tag == "default":
        tags = f"{tagsInUse[0]};{tagsInUse[1]};{tagsInUse[2]};{tagsInUse[3]};{tagsInUse[4]}"
    else:
        tags = f"{tag};{tagsInUse[0]};{tagsInUse[1]};{tagsInUse[2]};{tagsInUse[3]};{tagsInUse[4]};{tag}"

    models_quote = classifier(tags)

    check_for_profanity = profanity.censor(models_quote[0]["generated_text"])
    test_for_text = models_quote[0]["generated_text"].replace(" ", "x")

    while "*" in check_for_profanity or test_for_text == "xxxxxxxxx":
        models_quote = classifier(tags)

        check_for_profanity = profanity.censor(models_quote[0]["generated_text"])
        test_for_text = models_quote[0]["generated_text"].replace(" ", "x")

    return {"quote": models_quote[0]["generated_text"]}
