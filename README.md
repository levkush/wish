# Wish 🌟

![GitHub](https://img.shields.io/github/license/levkush/wish)
![GitHub last commit](https://img.shields.io/github/last-commit/levkush/wish)

A delightful wish list manager to keep track of your dreams and desires! ✨

## Description

Wish is a Python-based application built using Typer and Rich libraries. It serves as a wishlist manager that allows you to add, delete, and modify wishes. You can categorize wishes and mark them as completed or pending.

## Features

- Add wishes with categories
- Delete wishes from the list
- Modify wish properties (name, category, completion status)
- View wish list with sorting options

## Usage

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/username/repository.git
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Commands

- `wish add [name] [category]`: Add a new wish to the list.
- `wish delete [name]`: Delete a wish from the list.
- `wish set [name] [property] [value]`: Modify wish properties.
- `wish list [--sort | --category | --reverse | --all]`: Display the wish list with sorting options.

### Example Usage

#### Adding a Wish
```bash
wish add "Trip to Paris" "Travel"
```

#### Deleting a Wish
```bash
wish delete "Trip to Paris"
```

#### Modifying a Wish Property
```bash
wish set "Trip to Paris" "completed" "Yes"
```

#### Listing Wishes
```bash
wish list --sort --all
```

## Contributing

Feel free to contribute by opening issues or submitting pull requests. Your input is highly appreciated! 🙌

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
