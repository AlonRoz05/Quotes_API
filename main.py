from fastapi import FastAPI
from mangum import Mangum
from requests import post
from random import choice
from json import load

API_URL = "https://api-inference.huggingface.co/models/Rozi05/QuoteVibes_Model_Trained"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = post(API_URL, headers=headers, json=payload)
	return response.json()

with open("tags.json", "r") as file:
    tags_data = load(file)

app = FastAPI()
handler = Mangum(app)

@app.get("/")
async def root():
    return {"message" : "Please ensure you're on the correct page."}

@app.get("/get-quote/{tag}")
async def get_quote(tag: str):
    tagsInUse = []
    for _ in range(5):
        while True:
            chosen_tag = choice(tags_data["tags"])
            if (chosen_tag not in tagsInUse) and chosen_tag != tag:
                tagsInUse.append(chosen_tag)
                break

    tags = f"{tagsInUse[0]};{tagsInUse[1]};{tagsInUse[2]};{tagsInUse[3]};{tagsInUse[4]}"
    if tag != "default":
        tags = f"{tag};" + tags + f";{tag}"

    while True:
        models_quote = query({"inputs": tags})

        # here you need to check for profanity
        test_for_text = models_quote[0]["generated_text"].replace(" ", "x")

        if test_for_text != "xxxxxxxxx":
            return {"quote": models_quote[0]["generated_text"]}
