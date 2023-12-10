import requests
import random
import json

API_URL = "https://api-inference.huggingface.co/models/Rozi05/QuoteVibes_Model_Trained"
headers = {"Authorization": "Bearer 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"}

with open("tags.json", "r") as file:
    tags_data = json.load(file)

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def lambda_handler(event, context):
    input_tag = event['queryStringParameters']['input_tag']
    tagsInUse = [random.choice(tags_data["tags"]) for _ in range(5)]

    tags = ";".join(tagsInUse)
    if input_tag != "default":
        tags = f"{input_tag};{tags};{input_tag}"

    times_ran = 0
    while True:
        times_ran += 1
        models_quote = query({"inputs": tags})

        if models_quote != "         ": # and check for profanity
            break
        
        if times_ran >= 15:
            models_quote = [{"generated_text": "Sorry, Unable to generate any quotes for that tag. Please try again later."}]
            break

    response_body = {}
    response_body["quote"] = models_quote[0]["generated_text"]

    http_response = {}
    http_response["statusCode"] = 200
    http_response["headers"] = {}
    http_response["headers"]["Content-Type"] = "application/json"
    http_response["body"] = json.dumps(response_body)
    
    return http_response
