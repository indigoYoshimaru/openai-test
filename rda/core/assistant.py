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

        run = self.client.beta.threads.runs.create(
            thread_id=self.thread_id, assistant_id=self.assistant_id, stream=True,
        )

        for chunk in run:
            if type(chunk).__name__ != "ThreadMessageDelta":
                continue
            response_text = chunk.data.delta.content[0].text.value
            if response_text: 
                yield response_text

    @timer
    def predict(self, question: Text):
        self._create_user_message(question)