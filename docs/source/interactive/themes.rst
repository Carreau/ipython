
.. _themes:

======
Themes
======

IPython themes control the syntax highlighting and colors used in the terminal. Themes can be defined using either Python code (built-in) or JSON files (user-defined).

Using Themes
============

To set a theme in IPython, add this to ``ipython_config.py``:

.. code-block:: python

    c.InteractiveShell.colors = "linux"

Or at runtime in the IPython shell:

.. code-block:: python

    %colors linux


Built-in Themes
===============

IPython includes the following built-in themes:

- **nocolor** - Plain text without colors
- **neutral** - Default theme (adapts to platform)
- **linux** - Dark terminal colors (monokai-based)
- **lightbg** - Light background colors (pastie-based)
- **pride** - Full RGB colors with Unicode symbols
- **pride:l** - Light-background pride theme
- **gruvbox-dark** - Gruvbox colorscheme


JSON Theme Format
=================

You can define custom themes in JSON format without writing Python code. JSON theme files provide a simple, declarative way to define colors and styles.

File Location
-------------

Place JSON theme files in one of these directories:

1. ``~/.ipython/themes/`` (recommended for user themes)
2. ``./.ipython_themes/`` (local project themes)

JSON Schema
-----------

.. code-block:: json

    {
      "name": "my-theme",
      "base": "monokai",
      "colors": {
        "Token.Prompt": "ansibrightgreen",
        "Token.String": "ansiyellow"
      },
      "symbols": {
        "arrow_body": "-",
        "arrow_head": ">",
        "top_line": "-"
      }
    }

Fields
------

``name`` (required)
    The theme identifier. This is what you use when setting
    ``c.InteractiveShell.colors = "my-theme"``.

``base`` (optional)
    A Pygments style to use as the base. Available Pygments styles include:

    - ``monokai`` - Dark theme with vivid colors
    - ``pastie`` - Light theme
    - ``default`` - Neutral base
    - ``gruvbox-dark`` - Gruvbox colorscheme
    - Others from Pygments library

    If omitted or ``null``, no base style is used.

``colors`` (required)
    A mapping of Pygments token types to color/style values. Each key is a
    token type in the format ``Token.Category`` or
    ``Token.Category.SubCategory``.

    **Common Token Types:**

    - ``Token.Prompt`` - The primary prompt
    - ``Token.PromptNum`` - The prompt number
    - ``Token.OutPrompt`` - Output prompt
    - ``Token.OutPromptNum`` - Output prompt number
    - ``Token.String`` - String literals
    - ``Token.Comment`` - Comments
    - ``Token.Keyword`` - Python keywords
    - ``Token.Name`` - Variable/function names
    - ``Token.Number`` - Numeric literals
    - ``Token.Operator`` - Operators
    - ``Token.Header`` - Exception header
    - ``Token.ExcName`` - Exception name
    - ``Token.Filename`` - Filename in traceback
    - ``Token.Lineno`` - Line number in traceback
    - ``Token.Line`` - Code line in traceback

    See :ref:`token-types-reference` for the complete list.

    **Color/Style Values:**

    Colors can be specified as:

    - **ANSI colors**: ``ansired``, ``ansigreen``, ``ansiblue``, ``ansibrightred``, etc.
    - **RGB hex**: ``#FF5733``
    - **Named colors**: ``red``, ``green``, ``blue`` (requires 24-bit color support)
    - **Modifiers**: ``bold``, ``italic``, ``underline``
    - **Background**: ``bg:#FF5733`` or ``bg:ansired``
    - **Combined**: ``bold ansiblue``, ``bg:#FF0000 ansiwhite``

    **Available ANSI colors:**

    - Basic: ``ansired``, ``ansigreen``, ``ansiblue``, ``ansiyellow``, ``ansimagenta``, ``ansicyan``, ``ansiwhite``, ``ansiblack``
    - Bright: ``ansibrightred``, ``ansibrightgreen``, ``ansibrightblue``, ``ansibrightyellow``, ``ansibrightmagenta``, ``ansibrightcyan``, ``ansibrightwhite``

``symbols`` (optional)
    Customize the symbols used in tracebacks and debugger output. All fields
    are optional:

    - ``arrow_body`` - Character for arrow line (default: ``-``)
    - ``arrow_head`` - Character for arrow tip (default: ``>``)
    - ``top_line`` - Character for top border (default: ``-``)

    Example with Unicode:

    .. code-block:: json

        "symbols": {
          "arrow_body": "━",
          "arrow_head": "▶",
          "top_line": "━"
        }


Examples
========

Simple Dark Theme
-----------------

.. code-block:: json

    {
      "name": "my-dark",
      "base": "monokai",
      "colors": {
        "Token.Prompt": "ansibrightgreen",
        "Token.PromptNum": "ansigreen bold",
        "Token.OutPrompt": "ansibrightred",
        "Token.String": "ansiyellow",
        "Token.Comment": "ansibrightblack",
        "Token.Keyword": "ansiblue"
      }
    }

Custom Light Theme
-------------------

.. code-block:: json

    {
      "name": "my-light",
      "base": "pastie",
      "colors": {
        "Token.Prompt": "ansiblue",
        "Token.PromptNum": "ansiblue bold",
        "Token.OutPrompt": "ansired",
        "Token.String": "ansigreen",
        "Token.Comment": "ansibrightblack",
        "Token.Keyword": "ansired"
      }
    }

RGB Colors (24-bit)
-------------------

.. code-block:: json

    {
      "name": "my-rgb",
      "base": null,
      "colors": {
        "Token.Prompt": "#00FF00",
        "Token.String": "#00FFFF",
        "Token.Comment": "#808080",
        "Token.Keyword": "bold #FF00FF"
      }
    }

With Unicode Symbols
---------------------

.. code-block:: json

    {
      "name": "fancy",
      "base": "monokai",
      "colors": {
        "Token.Prompt": "ansibrightgreen",
        "Token.String": "ansiyellow"
      },
      "symbols": {
        "arrow_body": "━",
        "arrow_head": "▶",
        "top_line": "━"
      }
    }


.. _token-types-reference:

Token Types Reference
======================

General Tokens
--------------

=========================================  ==========================================
Token                                      Purpose
=========================================  ==========================================
``Token.Prompt``                           The main prompt marker
``Token.PromptNum``                        The number in the prompt
``Token.OutPrompt``                        Output prompt marker
``Token.OutPromptNum``                     The number in output prompt
=========================================  ==========================================

Traceback Display
-----------------

=========================================  ==========================================
Token                                      Purpose
=========================================  ==========================================
``Token.Header``                           Traceback header
``Token.ExcName``                          Exception name
``Token.Filename``                         Filename in traceback
``Token.FilenameEm``                       Highlighted filename
``Token.Lineno``                           Line number
``Token.LinenoEm``                         Highlighted line number
``Token.Line``                             Code line
``Token.Topline``                          Top border line
``Token.Caret``                            Caret symbol
=========================================  ==========================================

Syntax Highlighting
--------------------

=========================================  ==========================================
Token                                      Purpose
=========================================  ==========================================
``Token.String``                           String literals
``Token.Comment``                          Comments
``Token.Keyword``                          Keywords
``Token.Name``                             Names/identifiers
``Token.Name.Class``                       Class names
``Token.Name.Function``                    Function names
``Token.Number``                           Numbers
``Token.Operator``                         Operators
``Token.Error``                            Syntax errors
=========================================  ==========================================

Debugging
---------

=========================================  ==========================================
Token                                      Purpose
=========================================  ==========================================
``Token.Breakpoint``                       Breakpoint marker
``Token.Breakpoint.Enabled``               Enabled breakpoint
``Token.Breakpoint.Disabled``              Disabled breakpoint
=========================================  ==========================================

Special
-------

=========================================  ==========================================
Token                                      Purpose
=========================================  ==========================================
``Token.VName``                            Variable name in inspection
``Token.ValEm``                            Value emphasis
``Token.Normal``                           Normal text
``Token.NormalEm``                         Emphasized normal text
=========================================  ==========================================


Creating and Sharing Themes
============================

To create a custom theme:

1. Create a JSON file in ``~/.ipython/themes/`` directory
2. Name it descriptively (e.g., ``my-theme.json``)
3. Define the theme structure as shown above
4. Set it in your config: ``c.InteractiveShell.colors = "my-theme"``

The theme name is derived from the ``"name"`` field in the JSON, not the filename.


Migration from Python Themes
=============================

If you have a custom theme defined in Python, you can convert it to JSON:

**Python:**

.. code-block:: python

    custom_theme = Theme(
        "my-theme",
        "monokai",
        {
            Token.Prompt: "ansibrightgreen",
            Token.String: "ansiyellow",
        }
    )

**JSON equivalent:**

.. code-block:: json

    {
      "name": "my-theme",
      "base": "monokai",
      "colors": {
        "Token.Prompt": "ansibrightgreen",
        "Token.String": "ansiyellow"
      }
    }


Troubleshooting
===============

Theme not found
    Make sure the JSON file is in the correct directory and the filename is
    ``.json``. The theme name comes from the JSON ``"name"`` field, not the
    filename.

Colors not appearing
    - Ensure your terminal supports the colors you're using (ANSI colors work
      everywhere, RGB requires 24-bit support)
    - Check that the token type names are correct (use ``Token.Something``,
      not ``Something``)
    - Try a simpler theme to verify the system works

Invalid JSON
    Check that your JSON is valid:

    - All strings are quoted with double quotes
    - All keys and string values use double quotes
    - No trailing commas
    - Use a JSON validator online to check


See Also
========

- `Pygments Styles <https://pygments.org/styles/>`_ - Available base styles
- :doc:`/config/index` - IPython Configuration
