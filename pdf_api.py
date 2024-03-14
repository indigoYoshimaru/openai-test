# Upload a file with an "assistants" purpose
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("KEY")
assert api_key, "Empty key"
client = OpenAI(
    api_key=api_key,
)

file = client.files.create(file=open("data/manual.pdf", "rb"), purpose="assistants")

# Add the file to the assistant
assistant = client.beta.assistants.create(
    instructions="You are an engineer assistant in the refrigeration domain. Use the knowledge in the file to best respond to engineer queries. The response should be at most 300 words length.",
    model="gpt-3.5-turbo-0125",
    tools=[{"type": "retrieval"}],
    file_ids=[file.id],
)

thread = client.beta.threads.create()
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What are preventive measures to mitigate the risk of electric shock?",
    file_ids=[file.id],
)
run = client.beta.threads.runs.create(
    thread_id=thread.id, assistant_id=assistant.id, stream=True
)
for chunk in run:
    # print(chunk)
    if type(chunk).__name__ != "ThreadMessageDelta":
        continue
    response_text = chunk.data.delta.content[0].text.value

    print(response_text, end='')


# from time import sleep

# while run.status!='completed':
#     sleep(5)
#     run = client.beta.threads.runs.retrieve(
#     thread_id=thread.id,
#     run_id=run.id
#     )
# messages = client.beta.threads.messages.list(
#   thread_id=thread.id
# )

# # print(messages)

# from typing_extensions import override
# from openai import AssistantEventHandler

# # First, we create a EventHandler class to define
# # how we want to handle the events in the response stream.


# class EventHandler(AssistantEventHandler):
#     @override
#     def on_text_created(self, text) -> None:
#         print(f"\nassistant > ", end="", flush=True)

#     @override
#     def on_text_delta(self, delta, snapshot):
#         print(delta.value, end="", flush=True)

#     def on_tool_call_created(self, tool_call):
#         # print(f"\nassistant > {tool_call.type}\n", flush=True)
#         pass

#     def on_tool_call_delta(self, delta, snapshot):
#         # if delta.type == "code_interpreter":
#         #     if delta.code_interpreter.input:
#         #         print(delta.code_interpreter.input, end="", flush=True)
#         #     if delta.code_interpreter.outputs:
#         #         print(f"\n\noutput >", flush=True)
#         #         for output in delta.code_interpreter.outputs:
#         #             if output.type == "logs":
#         #                 print(f"\n{output.logs}", flush=True)
#         pass

# # Then, we use the `create_and_stream` SDK helper
# # with the `EventHandler` class to create the Run
# # and stream the response.

# with client.beta.threads.runs.create_and_stream(
#     thread_id=thread.id,
#     assistant_id=assistant.id,
#     event_handler=EventHandler(),
# ) as stream:
#     stream.until_done()

# ThreadMessageDelta(
#     data=MessageDeltaEvent(
#         id="msg_3AxFbS3vZMLppZpyk1EergU4",
#         delta=MessageDelta(
#             content=[
#                 TextDeltaBlock(
#                     index=0, type="text", text=TextDelta(annotations=None, value=" can")
#                 )
#             ],
#             file_ids=None,
#             role=None,
#         ),
#         object="thread.message.delta",
#     ),
#     event="thread.message.delta",
# )
