# -*- coding: utf-8 -*-
"""
Color schemes for exception handling code in IPython.
"""

import os

# *****************************************************************************
#       Copyright (C) 2005-2006 Fernando Perez <fperez@colorado.edu>
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
# *****************************************************************************

from IPython.utils.coloransi import ColorSchemeTable, TermColors, ColorScheme


def exception_colors():
    """Return a color table with fields for exception reporting.

    The table is an instance of ColorSchemeTable with schemes added for
    'Neutral', 'Linux', 'LightBG' and 'NoColor' and fields for exception handling filled
    in.

    Examples:

    >>> ec = exception_colors()
    >>> ec.active_scheme_name
    ''
    >>> print(ec.active_colors)
    None

    Now we activate a color scheme:
    >>> ec.set_active_scheme('NoColor')
    >>> ec.active_scheme_name
    'NoColor'


    .. >>> sorted(ec.active_colors.keys())
    .. ['Normal', 'breakpoint_disabled', 'breakpoint_enabled', 'caret', 'em',
    .. 'excName', 'filename', 'filenameEm', 'line', 'lineno', 'linenoEm', 'name',
    .. 'nameEm', 'normalEm', 'vName', 'val', 'valEm']

    """
    from pygments.token import Token

    ex_colors = ColorSchemeTable()

    # Populate it with color schemes
    C = TermColors  # shorthand and local lookup
    nc = ColorScheme(
        "NoColor",
        {
            # The colors to be used in the traceback
            "filename": C.NoColor,
            "lineno": C.NoColor,
            "name": C.NoColor,
            "val": C.NoColor,
            "em": C.NoColor,
            # Emphasized colors for the last frame of the traceback
            "normalEm": C.NoColor,
            "filenameEm": C.NoColor,
            "linenoEm": C.NoColor,
            "nameEm": C.NoColor,
            # Colors for printing the exception
            "excName": C.NoColor,
            "line": C.NoColor,
            "Normal": C.NoColor,
            # debugger
            "breakpoint_enabled": C.NoColor,
            "breakpoint_disabled": C.NoColor,
        },
    )
    nc.colors._pygments_equiv = {
        Token.LinenoEm: "",
        Token.Lineno: "",
        Token.ValEm: "",
        Token.VName: "",
        Token.Caret: "",
        Token.FilenameEm: "",
        Token.ExcName: "",
        Token.Topline: "",
    }
    ex_colors.add_scheme(nc)

    # make some schemes as instances so we can copy them for modification easily
    linux = ColorScheme(
        "Linux",
        {
            # The colors to be used in the traceback
            "filename": C.Green,
            "lineno": C.Green,
            "name": C.Purple,
            "val": C.Green,
            "em": C.LightCyan,
            # Emphasized colors for the last frame of the traceback
            "normalEm": C.LightCyan,
            "filenameEm": C.LightGreen,
            "linenoEm": C.LightGreen,
            "nameEm": C.LightPurple,
            # Colors for printing the exception
            "excName": C.LightRed,
            "line": C.Yellow,
            "Normal": C.Normal,
            # debugger
            "breakpoint_enabled": C.LightRed,
            "breakpoint_disabled": C.Red,
        },
    )
    # 2025: migration helper
    # temporary carry equivalent pygments token to style
    linux.colors._pygments_equiv = {
        Token.LinenoEm: "ansibrightgreen",
        Token.Lineno: "ansigreen",
        Token.ValEm: "ansibrightblue",
        Token.VName: "ansicyan",
        Token.Caret: "",
        Token.FilenameEm: "ansibrightgreen",
        Token.ExcName: "ansibrightred",
        Token.Topline: "ansibrightred",
    }
    ex_colors.add_scheme(linux)

    # For light backgrounds, swap dark/light colors
    lightbg = ColorScheme(
        "LightBG",
        {
            # The colors to be used in the traceback
            "filename": C.LightGreen,
            "lineno": C.LightGreen,
            "name": C.LightPurple,
            "val": C.LightGreen,
            "em": C.Cyan,
            # Emphasized colors for the last frame of the traceback
            "normalEm": C.Cyan,
            "filenameEm": C.Green,
            "linenoEm": C.Green,
            "nameEm": C.Purple,
            # Colors for printing the exception
            "excName": C.Red,
            # "line": C.Brown,  # brown often is displayed as yellow
            "line": C.Red,
            "Normal": C.Normal,
            # debugger
            "breakpoint_enabled": C.LightRed,
            "breakpoint_disabled": C.Red,
        },
    )
    lightbg.colors._pygments_equiv = {
        Token.LinenoEm: "ansigreen",
        Token.Lineno: "ansibrightgreen",
        Token.ValEm: "ansiblue",
        Token.VName: "ansicyan",
        Token.Caret: "",
        Token.FilenameEm: "ansigreen",
        Token.ExcName: "ansibrightred",
        Token.Topline: "ansired",
    }
    ex_colors.add_scheme(lightbg)

    neut = ColorScheme(
        "Neutral",
        {
            # The colors to be used in the traceback
            "filename": C.LightGreen,
            "lineno": C.LightGreen,
            "name": C.LightPurple,
            "val": C.LightGreen,
            "em": C.Cyan,
            # Emphasized colors for the last frame of the traceback
            "normalEm": C.Cyan,
            "filenameEm": C.Green,
            "linenoEm": C.Green,
            "nameEm": C.Purple,
            # Colors for printing the exception
            "excName": C.Red,
            # line = C.Brown,  # brown often is displayed as yellow
            "line": C.Red,
            "Normal": C.Normal,
            # debugger
            "breakpoint_enabled": C.LightRed,
            "breakpoint_disabled": C.Red,
        },
    )
    neut.colors._pygments_equiv = {
        Token.LinenoEm: "ansigreen",
        Token.Lineno: "ansibrightgreen",
        Token.ValEm: "ansiblue",
        Token.VName: "ansicyan",
        Token.Caret: "",
        Token.FilenameEm: "ansigreen",
        Token.ExcName: "ansibrightred",
        Token.Topline: "ansired",
    }
    ex_colors.add_scheme(neut)

    # Hack: the 'neutral' colours are not very visible on a dark background on
    # Windows. Since Windows command prompts have a dark background by default, and
    # relatively few users are likely to alter that, we will use the 'Linux' colours,
    # designed for a dark background, as the default on Windows.
    if os.name == "nt":
        ex_colors.add_scheme(ex_colors["Linux"].copy("Neutral"))

    return ex_colors
