import typer
import random
import flet as ft
from rda.configs.config_controller import EnvController, ConfigsController
from rda.core.assistant import Assistant
from rda.api.flet_app import FletApp
from rich.prompt import Prompt
from rich.console import Console

console = Console()

app = typer.Typer(no_args_is_help=True)


@app.command(help="How can I help you today?")
def chat(
    document_path: str = typer.Argument(
        default="",
        help="Tell me which document I can help you with. Enter to overwrite the document dir.",
    ),
    document_dir: str = typer.Argument(
        default="data/split", help="Directory to list of documents for reference"
    ),
    cfg_path: str = typer.Argument(
        default="rda/configs/configs.yaml", help="Path to the config file"
    ),
):
    env_controller = EnvController()
    user_name = env_controller.user_name
    if not user_name:
        while not user_name:
            user_name = Prompt.ask("Hello newcomer! Please enter your name to continue")
        env_controller.update(user_name)

    question = Prompt.ask(
        random.choice(
            [
                f"rda: Hello {user_name}, ask me anything\nUser",
                f"rda: Welcome to Refrigeration Diagnostic Assistant, {user_name}, how can I help you?\nUser",
                f"rda: Hey there {user_name}, happy to help! Questions, please!\nUser",
            ]
        )
    )

    cfg = ConfigsController(cfg_path)
    if document_path:
        bot = Assistant(
            cfg.assistant,
            document_paths=[document_path],
            key=env_controller.api_key,
        )
    else: 
        import os
        document_paths = [os.path.join(document_dir, fname) for fname in os.listdir(document_dir)]
        bot = Assistant(
            cfg.assistant,
            document_paths=document_paths,
            key=env_controller.api_key,
        )

    while True:
        answers = bot.get_stream_answer(question=question)
        console.print(f"rda: ", end="", style="bright_cyan")
        for answer in answers:
            console.print(answer, end="", style="bright_cyan", soft_wrap=True)

        question = Prompt.ask(
            random.choice(
                ["\nrda: Anything else?\nUser", "\nrda: Next questions, please!\nUser"]
            )
        )


@app.command(help="Evaluate my performance using your testset")
def eval(
    document_path: str = typer.Argument(
        default="data/manual.pdf", help="Tell me which document I can help you with"
    ),
    testset_path: str = typer.Argument(..., help="Directory to your test set please."),
    report_dir: str = typer.Argument(
        default="report", help="Directory to export the evaluation report"
    ),
):

    # tester = Tester(data_filepath=document_path)
    # # model = OpenAIAPI(model_name=model_name)
    # tester.run_testcases(
    #     model=model,
    #     report_filedir=report_dir,
    # )
    ...


@app.command(help="Start web app")
def run_app(
    document_path: str = typer.Argument(
        default="",
        help="Tell me which document I can help you with. Enter to overwrite the document dir.",
    ),
    document_dir: str = typer.Argument(
        default="data/split", help="Directory to list of documents for reference"
    ),
    cfg_path: str = typer.Argument(
        default="./configs/configs.yaml", help="Path to the config file"
    ),
):
    env_controller = EnvController()

    cfg = ConfigsController(cfg_path)

    if document_path:
        bot = Assistant(
            cfg.assistant,
            document_paths=[document_path],
            key=env_controller.api_key,
        )
    else: 
        import os
        document_paths = [os.path.join(document_dir, fname) for fname in os.listdir(document_dir)]
        bot = Assistant(
            cfg.assistant,
            document_paths=document_paths,
            key=env_controller.api_key,
        )

    flet_app = FletApp(
        config=cfg.flet,
        chatbot=bot,
    )

    ft.app(target=flet_app.run, view=ft.WEB_BROWSER, port=cfg.flet.port)
