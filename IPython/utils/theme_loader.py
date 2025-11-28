"""
JSON Theme Loader for IPython

This module provides functionality to load IPython themes from JSON files,
allowing themes to be defined without writing Python code.
"""

import json
from pathlib import Path

from pygments.token import Token, _TokenType

from .PyColorize import Theme, Symbols, _default_symbols


def _parse_token_string(token_str: str) -> _TokenType:
    """Parse a token type string to a Pygments Token object.

    Parameters
    ----------
    token_str : str
        Token type in dot notation (e.g., "Token.Prompt", "Token.Name.Class")

    Returns
    -------
    _TokenType
        Pygments Token object

    Raises
    ------
    ValueError
        If token_str does not start with "Token."

    Examples
    --------
    >>> _parse_token_string("Token.Prompt")
    Token.Prompt
    """
    parts = token_str.split(".")

    if not parts or parts[0] != "Token":
        raise ValueError(f"Invalid token string: {token_str}. Must start with 'Token.'")

    current = Token
    for part in parts[1:]:
        current = getattr(current, part)

    return current


def load_json_theme(json_path: str | Path) -> Theme:
    """Load a theme from a JSON file.

    The JSON file must contain "name" and "colors" fields. The "base" and
    "symbols" fields are optional. Token types in colors should use dot
    notation (e.g., "Token.Prompt").

    Parameters
    ----------
    json_path : str | Path
        Path to the JSON theme file

    Returns
    -------
    Theme
        Loaded theme object

    Raises
    ------
    FileNotFoundError
        If the JSON file doesn't exist
    ValueError
        If required fields are missing or token types are invalid
    """
    json_path = Path(json_path)

    if not json_path.exists():
        raise FileNotFoundError(f"Theme file not found: {json_path}")

    with open(json_path, "r") as f:
        data = json.load(f)

    if "name" not in data:
        raise ValueError("Theme JSON must have a 'name' field")
    if "colors" not in data:
        raise ValueError("Theme JSON must have a 'colors' field")

    name = data["name"]
    base = data.get("base")

    extra_style: dict[_TokenType, str] = {}
    for token_str, style in data["colors"].items():
        try:
            token = _parse_token_string(token_str)
            extra_style[token] = style
        except (ValueError, AttributeError) as e:
            raise ValueError(f"Invalid token in colors: {token_str}") from e

    symbols: Symbols | None = None
    if "symbols" in data:
        symbols_data = data["symbols"]
        symbols = Symbols(
            top_line=symbols_data.get("top_line", _default_symbols["top_line"]),
            arrow_body=symbols_data.get("arrow_body", _default_symbols["arrow_body"]),
            arrow_head=symbols_data.get("arrow_head", _default_symbols["arrow_head"]),
        )

    return Theme(name, base, extra_style, symbols=symbols)


def load_themes_from_directory(directory: str | Path) -> dict[str, Theme]:
    """Load all JSON theme files from a directory.

    Silently skips files that fail to load. Theme names are taken from the
    JSON "name" field, not the filename.

    Parameters
    ----------
    directory : str | Path
        Path to directory containing .json theme files

    Returns
    -------
    dict[str, Theme]
        Dictionary mapping theme names to Theme objects
    """
    directory = Path(directory)
    themes: dict[str, Theme] = {}

    if not directory.exists():
        return themes

    for json_file in directory.glob("*.json"):
        try:
            theme = load_json_theme(json_file)
            themes[theme.name] = theme
        except Exception as e:
            print(f"Warning: Failed to load theme from {json_file}: {e}")

    return themes


def get_default_theme_directories() -> list[Path]:
    """Get the default directories where user themes can be stored.

    Returns directories in order of precedence: IPython config directory first,
    then current working directory.

    Returns
    -------
    list[Path]
        List of theme directories
    """
    directories = []

    from IPython.paths import get_ipython_dir
    try:
        ipython_dir = Path(get_ipython_dir())
        theme_dir = ipython_dir / "themes"
        directories.append(theme_dir)
    except Exception:
        pass

    directories.append(Path.cwd() / ".ipython_themes")

    return directories
