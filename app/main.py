import crud, models
import telegram
from database import SessionLocal, engine

from rich.console import Console
from rich.table import Table
import typer

models.Base.metadata.create_all(bind=engine)
db = SessionLocal()
app = typer.Typer()
console = Console()


@app.command()
def board():
    airplanes = crud.airplanes(db)
    table = Table(title="Airplanes")
    table.add_column("Id")
    table.add_column("Name")
    table.add_column("Phone")
    table.add_column("Username")

    for airplane in airplanes:
        table.add_row(
            str(airplane.id), airplane.name, airplane.phone, airplane.username
        )

    console.print(table)


@app.command()
def park(
    api_id: int = typer.Argument(..., envvar="API_ID"),
    api_hash: str = typer.Argument(..., envvar="API_HASH"),
):
    api = telegram.API(api_id, api_hash)
    airplane = telegram.park(db, api)
    console.print(f"{airplane.id} was parked!")


@app.command()
def repark(
    api_id: int = typer.Argument(..., envvar="API_ID"),
    api_hash: str = typer.Argument(..., envvar="API_HASH"),
):
    api = telegram.API(api_id, api_hash)
    telegram.repark(db, api)
    board()


@app.command()
def soar(
    id: int,
    api_id: int = typer.Argument(None, envvar="API_ID"),
    api_hash: str = typer.Argument(None, envvar="API_HASH"),
):
    api = telegram.API(api_id, api_hash)
    messages = telegram.soar(db, id, api)
    table = Table(title="Last messages from Telegram", show_lines=True)
    table.add_column("text")
    table.add_column("date and time")

    for text, date in messages[-1::-1]:
        table.add_row(text, date.strftime("%d %b, %I:%M %p %Z"))

    console.print(table)


if __name__ == "__main__":
    app()
    db.close()
