"""Tools for coloring text in ANSI terminals.
"""

#*****************************************************************************
#       Copyright (C) 2002-2006 Fernando Perez. <fperez@colorado.edu>
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
#*****************************************************************************


import os
import warnings

from IPython.utils.ipstruct import Struct

__all__ = ["TermColors", "InputTermColors", "ColorScheme", "ColorSchemeTable"]


class TermColors:
    """Color escape sequences.

    This class defines the escape sequences for all the standard (ANSI?)
    colors in terminals. Also defines a NoColor escape which is just the null
    string, suitable for defining 'dummy' color schemes in terminals which get
    confused by color escapes.

    This class should be used as a mixin for building color schemes."""

    NoColor = ''  # for color schemes in color-less terminals.
    Normal = '\033[0m'   # Reset normal coloring

    Black = "\033[0;30m"
    Red = "\033[0;31m"
    Green = "\033[0;32m"
    Brown = "\033[0;33m"
    Blue = "\033[0;34m"
    Purple = "\033[0;35m"
    Cyan = "\033[0;36m"
    LightGray = "\033[0;37m"
    # Light colors
    DarkGray = "\033[1;30m"
    LightRed = "\033[1;31m"
    LightGreen = "\033[1;32m"
    Yellow = "\033[1;33m"
    LightBlue = "\033[1;34m"
    LightPurple = "\033[1;35m"
    LightCyan = "\033[1;36m"
    White = "\033[1;37m"
    # Blinking colors.  Probably should not be used in anything serious.
    BlinkBlack = "\033[5;30m"
    BlinkRed = "\033[5;31m"
    BlinkGreen = "\033[5;32m"
    BlinkYellow = "\033[5;33m"
    BlinkBlue = "\033[5;34m"
    BlinkPurple = "\033[5;35m"
    BlinkCyan = "\033[5;36m"
    BlinkLightGray = "\033[5;37m"


class ColorScheme:
    """Generic color scheme class. Just a name and a Struct."""

    name: str
    colors: Struct
    # 2025: migration helper
    # temporary carry equivalent pygments token to style
    _pygments_equiv: dict[type, str]

    def __init__(self, __scheme_name_, colordict=None):
        self.name = __scheme_name_
        self.colors = Struct(colordict)

    def copy(self,name=None):
        """Return a full copy of the object, optionally renaming it."""
        if name is None:
            name = self.name
        return ColorScheme(name, self.colors.dict())


class ColorSchemeTable(dict):
    """General class to handle tables of color schemes.

    It's basically a dict of color schemes with a couple of shorthand
    attributes and some convenient methods.

    active_scheme_name -> obvious
    active_colors -> actual color table of the active scheme"""

    def __init__(self, scheme_list=None, default_scheme=''):
        """Create a table of color schemes.

        The table can be created empty and manually filled or it can be
        created with a list of valid color schemes AND the specification for
        the default active scheme.
        """

        # create object attributes to be set later
        self.active_scheme_name = ''
        self.active_colors = None

        if scheme_list:
            if default_scheme == '':
                raise ValueError('you must specify the default color scheme')
            for scheme in scheme_list:
                self.add_scheme(scheme)
            self.set_active_scheme(default_scheme)

    def copy(self):
        """Return full copy of object"""
        return ColorSchemeTable(self.values(),self.active_scheme_name)

    def __setitem__(self, key: str, value: ColorScheme):
        assert isinstance(key, str)
        assert isinstance(value, ColorScheme)
        super().__setitem__(key, value)

    def add_scheme(self, new_scheme):
        """Add a new color scheme to the table."""
        if not isinstance(new_scheme, ColorScheme):
            raise ValueError('ColorSchemeTable only accepts ColorScheme instances')
        self[new_scheme.name] = new_scheme

    def set_active_scheme(self, scheme):
        """Set the currently active scheme.

        Names are compared in a case-insensitive way.
        """


        scheme_names = list(self.keys())
        valid_schemes = [s.lower() for s in scheme_names]
        scheme_test = scheme.lower()
        try:
            scheme_idx = valid_schemes.index(scheme_test)
        except ValueError as e:
            raise ValueError('Unrecognized color scheme: ' + scheme + \
                  '\nValid schemes: '+str(scheme_names).replace("'', ",'')) from e
        else:
            active = scheme_names[scheme_idx]
            self.active_scheme_name = active
            self.active_colors = self[active].colors
            # Now allow using '' as an index for the current active scheme
            self[''] = self[active]
