from pydantic import BaseModel
from typing import Any, List, Dict, Text, Union
import flet as ft


class Message(BaseModel):
    text: Text = ''
    user: Text
    message_type: Text


class ChatMessage(ft.Row):
    def __init__(
        self,
        message: Message,
        config: Dict,
        avatar_colors: List,
    ):
        super().__init__()
        color = self.get_avatar_color(message.message_type, avatar_colors)

        self.controls = [
            ft.Row(
                [
                    ft.CircleAvatar(
                        content=ft.Text(self.get_initials(message.message_type)),
                        color=ft.colors.WHITE,
                        bgcolor=color,
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                message.user,
                                weight="bold",
                                size=config["size"],
                                color=color,
                            ),
                            ft.Text(message.text, selectable=True, size=config["size"]),
                        ]
                    ),
                ],
                spacing=5,
                alignment=config["alignment"],
                wrap=True, 
            ),
        ]

    def get_initials(self, message_type: str):
        return message_type[:1].capitalize()

    def get_avatar_color(self, message_type: str, avatar_colors: List):
        return avatar_colors[hash(message_type) % len(avatar_colors)]