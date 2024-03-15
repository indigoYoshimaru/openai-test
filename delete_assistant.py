from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ.get("KEY")
assert api_key, "Empty key"
client = OpenAI(
    api_key=api_key,
)

my_assistants = client.beta.assistants.list(
    order="desc",
    limit=100,
).data

for assistant in my_assistants: 
    print(assistant.file_ids)
    response = client.beta.assistants.delete(assistant.id)
    print(response)

