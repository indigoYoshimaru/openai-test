import typer

# import flet as ft
# from app.model.configs import load_configs
# from app.api.flet_app import FletApp


app = typer.Typer(no_args_is_help=True)


@app.command(help="How can I help you today?")
def chat(
    document_path: str = typer.Argument(
        default="data/manual.pdf", help="Tell me which document I can help you with"
    ),
):
    import os
    import dotenv
    import random
    
    dotenv.load_dotenv()
    api_key = os.environ.get("KEY")
    assert api_key, "Empty key"
    user_name = os.environ.get("UNAME")
    while not user_name:
        user_name = typer.prompt("Hello newcomer! May I ask your name?")
    dotenv.set_key(".env", key_to_set="UNAME", value_to_set=user_name)

    question = typer.prompt(
        random.choice(
            [
                f"Hello {user_name}, ask me anything",
                f"Welcome to Refrigeration Diagnostic Assistant, {user_name}, how can I help you?",
                f"Hey there {user_name}, happy to help! Questions, please!",
            ]
        )
    )
    answer = "OK"
    while True:
        print(answer)
        question = typer.prompt(
            random.choice(["Anything else?", "Next questions, please!"])
        )


@app.command(help="Evaluate my performance using your testset")
def eval(
    document_path: str = typer.Argument(
        default="data/manual.pdf", help="Tell me which document I can help you with"
    ),
    testset_path: str = typer.Argument(..., help="Directory to your test set please."),
): ...


# def run_app():
#     # config_path = "app/config/config.yaml"
#     # configs = load_configs(config_path=config_path)

#     # flet_app = FletApp(
#     #     config=configs["flet_config"],
#     #     chatbot=chatbot,
#     # )
#     # ft.app(target=flet_app.run, view=ft.WEB_BROWSER, port=8080)
#     ...
