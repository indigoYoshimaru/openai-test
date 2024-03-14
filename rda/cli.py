import typer

# import flet as ft
# from app.model.configs import load_configs
# from app.api.flet_app import FletApp
import random
from rda.configs.config_controller import EnvController, ConfigsController
from rda.core.assistant import Assistant
app = typer.Typer(no_args_is_help=True)


@app.command(help="How can I help you today?")
def chat(
    document_path: str = typer.Argument(
        default="data/manual.pdf", help="Tell me which document I can help you with"
    ),
    cfg_path: str = typer.Argument(
        default="rda/configs/configs.yaml", help= "Path to the config file"
    )
):
    env_controller = EnvController()
    user_name = env_controller.user_name
    if not user_name:
        while not user_name:
            user_name = typer.prompt(
                "Hello newcomer! Please enter your name to continue"
            )
        env_controller.update(user_name)

    question = typer.prompt(
        random.choice(
            [
                f"rda: Hello {user_name}, ask me anything\nUser",
                f"rda: Welcome to Refrigeration Diagnostic Assistant, {user_name}, how can I help you?\nUser",
                f"rda: Hey there {user_name}, happy to help! Questions, please!\nUser",
            ]
        )
    )
    answer = "OK"
    cfg = ConfigsController(cfg_path)
    bot = Assistant(cfg.assistant, document_path=document_path, key=env_controller.api_key)

    while True:
        bot.get_stream_answer(question=question)
        question = typer.prompt(
            random.choice(["\nrda: Anything else?\nUser", "\nrda: Next questions, please!\nUser"])
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


# def run_app():
#     # config_path = "app/config/config.yaml"
#     # configs = load_configs(config_path=config_path)

#     # flet_app = FletApp(
#     #     config=configs["flet_config"],
#     #     chatbot=chatbot,
#     # )
#     # ft.app(target=flet_app.run, view=ft.WEB_BROWSER, port=8080)
#     ...
