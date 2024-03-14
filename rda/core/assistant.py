from typing import Text, Dict, List
from pydantic import BaseModel

from pydantic import BaseModel
from typing import Text, List, Dict, Any
from rda.utils.timer import timer
from loguru import logger
from typing_extensions import override
from openai import AssistantEventHandler, OpenAI


class Assistant(BaseModel):
    thread_id: Text
    document_id: Text
    assistant_id: Text
    client: Any

    def __init__(self, cfg: Dict, key: Text, document_path: Text):
        try:

            client = OpenAI(api_key=key)
            document = client.files.create(
                file=open(document_path, "rb"),
                purpose="assistants",
            )
            assistant = client.beta.assistants.create(
                **cfg,
                file_ids=[document.id],
            )
            thread = client.beta.threads.create()

        except Exception as e:
            logger.error(f"{type(e).__name__}: {e}")
            raise e
        else:
            super().__init__(
                client=client,
                document_id=document.id,
                thread_id=thread.id,
                assistant_id=assistant.id,
            )

    def _create_user_message(self, question: Text):
        try:
            message = self.client.beta.threads.messages.create(
                thread_id=self.thread_id,
                role="user",
                content=question,
                file_ids=[self.document_id],
            )

        except Exception as e:
            msg = f"{type(e).__name__}: {e}. Cannot create request to assistant"
            logger.error(msg)
            raise ConnectionError(msg)
        else:
            return message

    def get_stream_answer(self, question: Text):
        message = self._create_user_message(question)
        with self.client.beta.threads.runs.create_and_stream(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id,
            event_handler=EventHandler(),
        ) as stream:
            stream.until_done()
    @timer
    def predict(self, question: Text):
        self._create_user_message(question)


class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nrda: ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)
        # yield delta.value

    def on_tool_call_created(self, tool_call):
        pass

    def on_tool_call_delta(self, delta, snapshot):
        pass
