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

    for airplane in airplanes:
        table.add_row(str(airplane.id), airplane.user_name)

    console.print(table)


@app.command()
def park():
    airplane = telegram.park(db)
    console.print(f"{airplane.id} was parked!")


@app.command()
def soar(id: int):
    messages = telegram.soar(db, id)
    table = Table(title="Last messages from Telegram", show_lines=True)
    table.add_column("text")
    table.add_column("date and time")

    for text, date in messages[-1::-1]:
        table.add_row(text, date.strftime("%d %b, %I:%M %p %Z"))

    console.print(table)


if __name__ == "__main__":
    app()
    db.close()
