# Copyright 2021 Oskar Sharipov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

import hjson
import typer
from rich.console import Console
from rich.table import Table

from . import __version__
from . import crud, models, telegram, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
db = SessionLocal()
console = Console()
app = typer.Typer(help="Hangar of Telegram accounts.")


@app.command()
def version():
    """
    Print version.
    """

    console.print(__version__)


@app.command()
def export():
    """
    Export data with secret tokens.
    """

    airplanes = [x.dict() for x in crud.airplanes(db)]
    hjson.dump(airplanes, sys.stdout)


@app.command("import")
def import_():
    """
    Erase database and import exported before data.
    """

    raw_airplanes = hjson.load(sys.stdin)
    try:
        airplanes = [schemas.AirplaneCreate(**x) for x in raw_airplanes]
    except:
        console.print("Incorrect input.")
        return

    for airplane in crud.airplanes(db):
        crud.destroy_airplane(db, airplane)
    for airplane in airplanes:
        _ = crud.build_airplane(db, airplane)
    console.print("Data is imported successfully.")


@app.command()
def track():
    """
    Show a table with every parked account.
    """

    airplanes = crud.airplanes(db)
    table = Table(title="Accounts")
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
    """
    Add an account in database.
    """

    api = telegram.API(api_id, api_hash)
    airplane = telegram.park(db, api)
    if airplane:
        console.print(f"{airplane.id} was parked!")
    else:
        console.print("Couldn't park an account.")


@app.command()
def unpark(id: int):
    """
    Remove an account from database.
    """

    airplane = crud.airplane_by_id(db, id)
    crud.destroy_airplane(db, airplane)
    console.print(f"{airplane.id} was unparked!")


@app.command()
def repark(
    api_id: int = typer.Argument(..., envvar="API_ID"),
    api_hash: str = typer.Argument(..., envvar="API_HASH"),
):
    """
    Update information about parked accounts.
    """

    api = telegram.API(api_id, api_hash)
    telegram.repark(db, api)
    track()


@app.command()
def soar(
    id: int,
    api_id: int = typer.Argument(None, envvar="API_ID"),
    api_hash: str = typer.Argument(None, envvar="API_HASH"),
):
    """
    Show last service messages of an account.
    """

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
