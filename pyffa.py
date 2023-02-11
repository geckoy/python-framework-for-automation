#!/usr/bin/env python3
import typer
from App.Helpers import *
app = typer.Typer()



@app.command()
def start(supervisor:str = "cli", debug: bool = typer.Option(False, help="Start app in debug mode." ), specific_processes:str = typer.Option("", help="Specific process to execute, e.g. python pyffa.py start --specific-processes=vpsample,psample"), specific_env:str = typer.Option("", help="Specific settings.json file to retreive env var's from, e.g. python pyffa.py start --specific-env=settings_test.json")):
    if specific_env: add2memory(specific_env=specific_env)
    start_application(supervisor, debug, **{"specific_processes":specific_processes, "specific_env":specific_env})
    
@app.command()
def stop(specific_env:str = typer.Option("", help="Specific settings.json file to retreive env var's from, e.g. python pyffa.py stop --specific-env=settings_test.json")):
    if specific_env: add2memory(specific_env=specific_env)
    exec_command("manage_app","stop_app")

@app.command()
def migration(purpose:str = "runAll", specific_env:str = typer.Option("", help="Specific settings.json file to retreive env var's from, e.g. python pyffa.py migration --purpose=runAll --specific-env=settings_test.json")):
    if specific_env: add2memory(specific_env=specific_env)
    Dbmigration(purpose)

@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command()
def goodbye(name: str = typer.Argument("User"), formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()
