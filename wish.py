from typing import Optional
from rich.console import Console
import typer
from rich.table import Column, Table
from rich.theme import Theme
from pathlib import Path
import os

# Define a color scheme for the console
color_scheme = Theme({
    "red": "#af00ff",
    "warning": "magenta",
    "danger": "bold red"
})

# Create a Typer app instance, a Rich console instance, and a Rich table for displaying wish list data
app = typer.Typer()
console = Console(color_system="truecolor", theme=color_scheme)
table = Table(
    Column("Wish", justify="left", width=30),
    Column("Category", justify="center"),
    Column("Completed?", justify="center", width=11),
    header_style="cyan bold",
    title="My Wish List",
)

# Define metadata for the application
__app_name__ = "Wish"
__version__ = "0.0.1"
__save__ = "./wishlist"  # Path.home() / "wish" / "wishlist"

# Ensure that the directory for saving wishlist files exists
os.makedirs(Path.home() / "wish", exist_ok=True)

# Function to convert table columns to rows
def get_rows():
    rows = table.columns

    vertical = []

    for row in rows:
        vertical.append([str(cell) for cell in row.cells])

    out = []

    for count in range(len(vertical[0])):
        out.append([vertical[row][count] for row in range(len(rows))])

    return out

# Function to load wishlist data from a file
def load():
    with open(__save__) as f:
        lines = f.readlines()

    for line in lines:
        try:
            line = line.replace("\n", "").split(" ")

            difficulty = line.pop(-2)
            status = line.pop(-1)
            wish = " ".join(word for word in line)

            table.add_row(wish, difficulty, status)
        except Exception:
            continue

# Function to save wishlist data to a file
def save():
    with open(__save__, "w") as f:
        for row in get_rows():
            f.write(" ".join(row) + "\n")

# Function to determine the sorting key for category
def sort_category(key, categories):
    key = key[-2]

    for idx, category in enumerate(categories):
        if key == category:
            return idx

    return 1

# Function to determine the sorting key for completion status
def sort_completed(key, categories):
    return int(key)

# Function to get wishes
def get_wish(name: str):
    rows = get_rows()
    finds = []
    name = name.lower()

    for row in rows:
        row = row[0].lower()

        if name in row:
            finds.append(row)
    
    if len(finds) == 0:
        return None
    
    if len(finds) == 1:
        return name
    
    if len(finds) > 1:
        for find in finds:
            if find == name:
                return find
    
    return finds[0]

# Load and save wishlist data
load()
save()

# Define the main command for the application
@app.command(help="Main command for the application.")
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        is_eager=True
    )
):
    print(version)
    return True

# Define the 'add' command to create a new wish
@app.command(name="add", help="Add a new wish to the wish list.", no_args_is_help=True)
def add(name: str, category: str):
    if get_wish(name) is not None:
        print(f"\n\n🛑 Sorry, but wish '{name}' already exists in your wish list! 😔\n\n")

        return

    table.add_row(name, category, "False")
    save()
    print(f"\n✨ Wish '{name}' in category '{category}' added successfully! 🌟\n")

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
        Column("Wish", justify="left", width=30),
        Column("Category", justify="center"),
        Column("Completed?", justify="center", width=11),
        header_style="cyan bold",
        title="My Wish List",
    )

    for row in sorted_rows:
        difficulty = row.pop(-2)
        status = row.pop(-1)

        # Add a row to the sorted table
        sorted_table.add_row(" ".join(row), difficulty, status)

    # Display the sorted table
    print("\n")
    console.print(sorted_table)
    print("\n")

# Run the Typer app if the script is executed
if __name__ == "__main__":
    app()