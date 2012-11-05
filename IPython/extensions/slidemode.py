# -*- coding: utf-8 -*-
"""
%slidemode magic for notebook
"""
#-----------------------------------------------------------------------------
#  Copyright (c) 2012, The IPython Development Team.
#
#  Distributed under the terms of the Modified BSD License.
#
#  The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

from IPython.core.display import HTML, Javascript, display_javascript
from IPython.core.magic import Magics, magics_class, line_magic
from IPython.testing.skipdoctest import skip_doctest
#-----------------------------------------------------------------------------
# Functions and classes
#-----------------------------------------------------------------------------
### big  JS file
import io
import os

path = os.path.realpath(__file__)
print(path)

f = io.open('.'.join(path.split('.')[:-1] + ['js']))

js= f.read()

##
@magics_class
class StoreMagics(Magics):

    @skip_doctest
    @line_magic
    def slideshow_mode(self, parameter_s=''):
        display_javascript(Javascript(js))


_loaded = False

def load_ipython_extension(ip):
    """Load the extension in IPython."""
    global _loaded
    if not _loaded:
        ip.register_magics(StoreMagics)
        _loaded = True
