import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS package
import tiktoken
import openai

app = Flask(__name__)
CORS(app)  # Enable CORS for your Flask app and specify allowed origins

openai.api_type = "azure"
openai.api_version = "2023-03-15-preview" 
openai.api_base = "YOUR_AZURE_OPENAI_API_KEY"
openai.api_key = "YOUR_AZURE_OPENAI_RESOURCE_ENDPOINT"

deployment_name = "cs-chat"

max_response_tokens = 250
token_limit= 4000

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens

@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input')
    conversation = request.json.get('conversation', [{"role": "system", "content": "You are a helpful assistant."}])

    conversation.append({"role": "user", "content": user_input})

    num_tokens = num_tokens_from_messages(conversation)
    while (num_tokens+max_response_tokens >= token_limit):
        del conversation[1] 
        num_tokens = num_tokens_from_messages(conversation)


    response = openai.ChatCompletion.create(
        engine="model-chat", # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.
        messages = conversation,
        temperature=0.7,
        max_tokens=token_limit,
    )

    conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    return jsonify(conversation)

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)