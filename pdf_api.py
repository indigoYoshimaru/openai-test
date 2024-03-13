# Upload a file with an "assistants" purpose
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
assert api_key, "Empty key"
client = OpenAI(
    api_key=api_key,
)

file = client.files.create(
  file=open("data/manual.pdf", "rb"),
  purpose='assistants'
)

# Add the file to the assistant
assistant = client.beta.assistants.create(
  instructions="You are an engineer assistant in the refrigeration domain. Use the knowledge in the file to best respond to engineer queries. The response should be at most 300 words length.",
  model="gpt-3.5-turbo-0125",
  tools=[{"type": "retrieval"}],
  file_ids=[file.id]
)

thread = client.beta.threads.create()
message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role="user",
    content="What are preventive measures to mitigate the risk of electric shock?",
    file_ids=[file.id]
)
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
)

from time import sleep
while run.status!='completed': 
    sleep(5)
    run = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
    )
messages = client.beta.threads.messages.list(
  thread_id=thread.id
)
print(messages)