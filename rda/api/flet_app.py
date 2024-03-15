from rda.configs.config_controller import FletConfig
from rda.core.ft import Message, ChatMessage
from rda.core.assistant import Assistant
from pydantic import BaseModel
import flet as ft
from loguru import logger


class FletApp(BaseModel):
    config: FletConfig
    chatbot: Assistant

    class Config:
        arbitrary_types_allowed = True

    def run(self, page: ft.Page):
        try:
            session_id = page.client_storage.get(page.client_ip)
            assert session_id, "No session id found. Checking for registration..."
        except AssertionError as e:
            logger.warning(f"{type(e).__name__}: {e}")
            page.client_storage.set(page.client_ip, page.session_id)

        def send_click(e):
            msg = chat_box.value
            chat_box.value = ""
            chat.controls += ChatMessage(
                Message(
                    user=page.client_storage.get(page.client_ip),
                    text=msg,
                    message_type="User",
                ),
                config=self.config.user_message,
                avatar_colors=self.config.avatar_colors,
            ).controls

            page.update()

            response_chunk = self.chatbot.get_stream_answer(
                question=msg,
            )

            chat.controls += ChatMessage(
                Message(
                    user=self.config.bot_message["name"],
                    text="",
                    message_type="Bot",
                ),
                config=self.config.bot_message,
                avatar_colors=self.config.avatar_colors,
            ).controls
            for response in response_chunk:
                chat.controls[-1].controls[-1].controls[-1].value += response
                page.update()

        try:
            page.title = self.config.title
            chat = ft.ListView(**self.config.chat_view)
            chat_box = ft.TextField(**self.config.chat_box, on_submit=send_click)
            page.add(
                ft.Row(
                    controls=[ft.Text(**self.config.header)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(content=chat, **self.config.container),
                ft.Row(
                    controls=[
                        chat_box,
                        ft.IconButton(
                            icon=ft.icons.SEND_ROUNDED,
                            tooltip="Send message",
                            on_click=send_click,
                        ),
                    ]
                ),
            )
            page.update()
        except Exception as e:
            logger.error(f"{type(e).__name__}: {e} happened. Cannot create Flet page")
            raise e
