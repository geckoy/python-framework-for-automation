#!/usr/bin/env python3
import typer
from App.Helpers import *
app = typer.Typer()



@app.command()
def start(supervisor:str = "cli", debug: bool = typer.Option(False, help="Start app in debug mode." )):
    start_application(supervisor, debug)
    
    
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
