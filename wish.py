#!/usr/bin/env python3

import random
from typing import Optional
from rich.console import Console
import typer
from rich.table import Column, Table
from rich.theme import Theme
from pathlib import Path
import os
from typing_extensions import Annotated

# Define a color scheme for the console
color_scheme = Theme({
    "#FF6B66": "#af00ff",
    "warning": "magenta",
    "danger": "bold #FF6B66"
})

# Create a Typer app instance, a Rich console instance, and a Rich table for displaying wish list data
app = typer.Typer()
console = Console(color_system="truecolor", theme=color_scheme)
table = Table(
    Column("Wish", justify="left", width=30, style="#FFD166"),
    Column("Category", justify="center", style="#06D6A0"),
    Column("Completed?", justify="center", width=10),
    header_style="#66C2FF bold",
    title="My Wish List",
)

# Define metadata for the application
__app_name__ = "Wish"
__version__ = "0.0.1"
__save__ = Path.home() / "wish" / "wishlist"

# Ensure that the directory for saving wishlist files exists
os.makedirs(Path.home() / "wish", exist_ok=True)

# Function to convert table columns to rows
def get_rows():
    rows = table.columns

    vertical = []

    for row in rows:
        vertical.append([str(cell) for cell in row.cells])

    out = []
    
    try:
        for count in range(len(vertical[0])):
            out.append([vertical[row][count] for row in range(len(rows))])
    except Exception:
        return []

    return out

# Function to load wishlist data from a file
def load():
    try:
        with open(__save__) as f:
            lines = f.readlines()
    except Exception:
        with open(__save__, "w") as f:
            pass

        with open(__save__) as f:
            lines = f.readlines()

    for line in lines:
        try:
            line = line.replace("\n", "").split(" ")

            category = line.pop(-2)
            completed = line.pop(-1)

            wish = " ".join(word for word in line)

            if completed != "True" and completed != "False":
                completed = "False"

            table.add_row(wish, category, completed)
        except Exception:
            continue

# Function to save wishlist data to a file
def save(ignore: list = None, edit: list = None):
    if ignore is None:
        ignore = []

    with open(__save__, "w") as f:
        for row in get_rows():
            if row[0] in ignore:
                continue

            if edit is not None:
                if row[0] == edit[0]:
                    row[edit[1]] = edit[2]

            f.write(" ".join(row) + "\n")

# Function to determine the sorting key for category
def sort_category(key, categories):
    key = key[-2]

    for idx, category in enumerate(categories):
        if key == category:
            return idx

    return 1

# Function to determine the sorting key for completion completed
def sort_completed(key, categories):
    return int(key)

# Function to get wishes
def get_wish(name: str):
    rows = get_rows()
    finds = []
    name = name.lower()

    for row in rows:
        row = row[0]

        if name in row.lower():
            finds.append(row)
    
    if len(finds) == 0:
        return None
    
    if len(finds) == 1:
        return finds[0]
    
    if len(finds) > 1:
        for find in finds:
            if find == name:
                return find
    
    return finds[0]

def random_prefix(prefix_list):
    return random.choice(prefix_list)

def version_callback(value: bool):
    if value:
        console.print(f"\n👋 Hi, I am [#66C2FF bold]wish v{__version__}[/#66C2FF bold] created by [bold #66C2FF]levkush[/bold #66C2FF].\n\n🪄  I am a program that will make your wish list! 🔮\n")
        raise typer.Exit()

# Load and save wishlist data
load()
save()

# Define the main command for the application
@app.callback()
def main(
    version: Annotated[
        Optional[bool], typer.Option("--version", "-v", callback=version_callback)
    ] = None,
):
    print(version)

# Define the 'add' command to create a new wish
@app.command(name="add", help="Add a new wish to the wish list.", no_args_is_help=True)
def add(name: str, category: str):
    name = name.capitalize()

    if get_wish(name) is not None:
        print(f"\n\n🛑 Sorry, but wish '{name}' already exists in your wish list! 😔\n\n")

        return

    table.add_row(name, category, "False")
    save()
    print(f"\n✨ Wish '{name}' in category '{category}' added successfully! 🌟\n")

# Define the 'delete' command to delete a wish
@app.command(name="delete", help="Delete a wish from the wish list.", no_args_is_help=True)
def delete(name: str):
    name = name.capitalize()
    target = get_wish(name)

    if target is None:
        prefix = random_prefix(["[bold #FF6B66]Can't find it![/bold #FF6B66]", "[bold #FF6B66]Where is it?[/bold #FF6B66]", "[bold #FF6B66]Lost forever![/bold #FF6B66]", "[bold #FF6B66]It's gone![/bold #FF6B66]"])
        console.print(f"\n🛑 {prefix} Wish [#66C2FF]'{name}'[/#66C2FF] is not in your wish list! 😔\n")

        return

    save(ignore=get_wish(name))
    load()

    prefix = random_prefix(["[bold #FF6B66]Throw away![/bold #FF6B66]", "[bold #FF6B66]Flaming hot![/bold #FF6B66]", "[bold #FF6B66]Into the bin![/bold #FF6B66]", "[bold #FF6B66]It belongs there![/bold #FF6B66]"])
    console.print(f"\n🗑  {prefix} Wish [#66C2FF]'{target}'[/#66C2FF] deleted successfully! 🔥\n")

# Define the 'set' command to assign wish property to a value.
@app.command(name="set", help="Assign wish property to a value.", no_args_is_help=True)
def set_(
    name: Annotated[str, typer.Argument(help="The name of the wish to edit")], 
    property: Annotated[str, typer.Argument(help="The edit property. Properties: category, completed, name.")], 
    value: Annotated[str, typer.Argument(help="The edit value. Values: <name>, <category>, yes, no.")]
):
    name = name.capitalize()
    target = get_wish(name)
    value = value.capitalize()

    property = property.lower()

    if target is None:
        prefix = random_prefix(["[bold #FF6B66]Can't find it![/bold #FF6B66]", "[bold #FF6B66]Where is it?[/bold #FF6B66]", "[bold #FF6B66]Lost forever![/bold #FF6B66]", "[bold #FF6B66]It's gone![/bold #FF6B66]"])
        console.print(f"\n🛑 {prefix} Wish [#66C2FF]'{name}'[/#66C2FF] is not in your wish list! 😔\n")

        return

    if property == "completed":
        if value == "Yes":
            value = 'True'

        elif value == "No":
            value = 'False'

        if value != "True" and value != "False":
            value = "False"

        save(edit=[target, 2, value])
    elif property == "name":
        save(edit=[target, 0, value])
    elif property == "category":
        save(edit=[target, 1, value.capitalize()])
    else:
        prefix = random_prefix(["[bold #FF6B66]Can't find it![/bold #FF6B66]", "[bold #FF6B66]Where is it?[/bold #FF6B66]", "[bold #FF6B66]Lost forever![/bold #FF6B66]", "[bold #FF6B66]It's gone![/bold #FF6B66]"])
        console.print(f"\n🛑 {prefix} Property [#66C2FF]'{property}'[/#66C2FF] doesn't exist! 😔\n")
    load()

    prefix = random_prefix(["[bold #06D6A0]Edit Successful![/bold #06D6A0]", "[bold #06D6A0]Good as new![/bold #06D6A0]", "[bold #06D6A0]Changes![/bold #06D6A0]", "[bold #06D6A0]Misspelled?[/bold #06D6A0]"])
    console.print(f"\n📝 {prefix} Wish [#66C2FF]'{target}'[/#66C2FF] property [#66C2FF]'{property}'[/#66C2FF] set to [#66C2FF]'{value}'[/#66C2FF] successfully! 🖊️\n")

# Define the 'list' command for displaying the wish list
@app.command(name="list", help="Display the wish list.")
def list_(
    alpha: Optional[bool] = typer.Option(
        True,
        "--sort",
        "-w",
        help="Sort alphabetically by wish names.",
    ),
    category: Optional[bool] = typer.Option(
        False,
        "--category",
        "-c",
        help="Sort alphabetically by category names.",
    ),
    reverse: Optional[bool] = typer.Option(
        False,
        "--reverse",
        "-r",
        help="Sort in reverse.",
    ),
    all: Optional[bool] = typer.Option(
        None,
        "--all",
        "-a",
        help="Show already completed wishes.",
    )
):
    rows_old = get_rows()
    rows = []

    if not all:
        for row in rows_old:
            if row[-1] == "False":
                rows.append(row)
    else:
        rows = rows_old

    sorted_rows = []

    if all and category:
        categories = sorted(set(row[-2] for row in rows))
        sorted_rows = sorted(rows, key=lambda x: (int(x[-1] == "True"), sort_category(x, categories)), reverse=reverse)

    elif all and alpha:
        sorted_rows = sorted(rows, key=lambda x: (int(x[-1] == "True"), x), reverse=reverse)

    elif category:
        categories = sorted(set(row[-2] for row in rows))
        sorted_rows = sorted(rows, key=lambda x: sort_category(x, categories), reverse=reverse)

    elif alpha:
        sorted_rows = sorted(rows, reverse=reverse)

    # Create a new table for sorted data
    sorted_table = Table(
        Column("Wish", justify="left", width=30, style="#FFD166"),
        Column("Category", justify="center", style="#06D6A0"),
        Column("Completed?", justify="center", width=10),
        header_style="#66C2FF bold",
        title="My Wish List",
    )

    for row in sorted_rows:
        category = row.pop(-2)
        completed = row.pop(-1)

        if completed == 'True':
            completed = "✅"
        else:
            completed = "❌"

        # Add a row to the sorted table
        sorted_table.add_row(" ".join(row), category, completed)

    # Display the sorted table
    print("\n")
    console.print(sorted_table)
    print("\n")

# Run the Typer app if the script is executed
if __name__ == "__main__":
    app()