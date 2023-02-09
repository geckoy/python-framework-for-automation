#!/usr/bin/env python3
import typer
from App.Helpers import *
app = typer.Typer()



@app.command()
def start(supervisor:str = "cli", debug: bool = typer.Option(False, help="Start app in debug mode." ), specific_processes:str = typer.Option("", help="Specific process to execute, e.g. python pyffa.py start --specific-processes=vpsample,psample")):
    start_application(supervisor, debug, specific_processes)
    
    
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
