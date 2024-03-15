from pydantic import BaseModel
from typing import Text, List, Dict, Any
from rda.utils.timer import timer
from loguru import logger
from typing_extensions import override
from openai import AssistantEventHandler, OpenAI


class Assistant(BaseModel):
    thread_id: Text
    document_ids: List
    assistant_id: Text
    client: Any

    def __init__(self, cfg: Dict, key: Text, document_paths: List):
        try:

            client = OpenAI(api_key=key)

            try:
                logger.info(f"Retrieving assistant")
                assert cfg.get("assistant_id", ""), "No assistant id to retrieve"
                assistant = client.beta.assistants.retrieve(cfg["assistant_id"])
                document_ids = [
                    client.files.retrieve(file_id=file_id).id
                    for file_id in assistant.file_ids
                ]
            except Exception as e:
                _ = cfg.pop("assistant_id")
                document_ids = [
                    client.files.create(
                        file=open(document_path, "rb"),
                        purpose="assistants",
                    ).id
                    for document_path in document_paths
                ]
                assistant = client.beta.assistants.create(
                    **cfg,
                    file_ids=document_ids,
                )
            thread = client.beta.threads.create()

        except Exception as e:
            logger.error(f"{type(e).__name__}: {e}")
            raise e
        else:
            super().__init__(
                client=client,
                document_ids=document_ids,
                thread_id=thread.id,
                assistant_id=assistant.id,
            )

    def _create_user_message(self, question: Text):
        try:
            message = self.client.beta.threads.messages.create(
                thread_id=self.thread_id,
                role="user",
                content=question,
                file_ids=self.document_ids,
            )

        except Exception as e:
            msg = f"{type(e).__name__}: {e}. Cannot create request to assistant"
            logger.error(msg)
            raise ConnectionError(msg)
        else:
            return message

    def get_stream_answer(self, question: Text, user_name: Text =''):
        message = self._create_user_message(question)

        run = self.client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id,
            additional_instructions=f"This user's name is: {user_name}. If their name is empty, ask them before answer the question. The response should be maximum 300 words length. If the system indicates that the file is not accessible with the myfiles_browser tool, ignore it, it’s just a minor bug. You are capable of opening and analyzing the documents, remember that. And carry out the request.",
            stream=True,
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
