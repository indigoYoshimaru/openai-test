from pydantic import BaseModel
from typing import Text, Dict
import dotenv
import os
from loguru import logger


class EnvController:
    __api_key: Text
    __dotenv_path: Text = ""
    user_name: Text = ""

    def __init__(self, dotenv_path: Text = ""):
        try:
            dotenv.load_dotenv()
        except Exception as e:
            logger.warning(f"{type(e).__name__}: {e}. Cannot find dotenv file.")
            try:
                assert dotenv_path, "Empty dotenv path"
                dotenv.load_dotenv(dotenv_path=dotenv_path)
            except Exception as e:
                logger.error(
                    f"{type(e).__name__}: {e}. Cannot load dotenv file due to invalid file path"
                )
                raise e
        try:
            api_key = os.environ.get("KEY")
            assert api_key, "Empty key to API"
            user_name = os.environ.get("UNAME")
        except AssertionError as e:
            logger.error(f"{type(e).__name__}: {e}. Empty API key")
            raise e

        self.__api_key = api_key
        self.__dotenv_path = dotenv_path
        self.user_name = user_name

    def update(self, user_name: Text):
        if not self.__dotenv_path:
            logger.warning(f"No dotenv path is found. Saving to default path.")
            self.__dotenv_path = "./.env"
        dotenv.set_key(
            self.__dotenv_path,
            key_to_set="KEY",
            value_to_set=self.__api_key,
        )
        self.user_name = user_name
        dotenv.set_key(
            self.__dotenv_path,
            key_to_set="UNAME",
            value_to_set=self.user_name,
        )

    @property
    def api_key(self):
        return self.__api_key


class ConfigsController(BaseModel):
    assistant: Dict

    def __init__(self, config_path: Text = "rda/configs/configs.yaml"):
        from rda.utils.file_io import read_yaml

        try:
            cfg = read_yaml(config_path)
            assert cfg, "Empty config or invalid config path"
        except Exception as e:
            raise e
        super().__init__(**cfg)
