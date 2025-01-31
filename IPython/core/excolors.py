"""
Color schemes for exception handling code in IPython.
"""

# *****************************************************************************
#       Copyright (C) 2005-2006 Fernando Perez <fperez@colorado.edu>
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
# *****************************************************************************

from IPython.utils.PyColorize import ANSICodeColors


def exception_colors():
    """Return a color table with fields for exception reporting."""
    return ANSICodeColors
