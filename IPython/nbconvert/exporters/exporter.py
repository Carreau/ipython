"""This module defines Exporter, a highly configurable converter
that uses Jinja2 to export notebook files into different formats.
"""

#-----------------------------------------------------------------------------
# Copyright (c) 2013, the IPython Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

from __future__ import print_function, absolute_import

# Stdlib imports
import io
import os
import inspect
import copy
import collections
import datetime

# other libs/dependencies
from jinja2 import Environment, FileSystemLoader, ChoiceLoader

# IPython imports
from IPython.config.configurable import Configurable
from IPython.config import Config
from IPython.nbformat import current as nbformat
from IPython.utils.traitlets import MetaHasTraits, DottedObjectName, Unicode, List, Dict
from IPython.utils.importstring import import_item
from IPython.utils.text import indent
from IPython.utils import py3compat

from IPython.nbconvert import transformers as nbtransformers
from IPython.nbconvert import filters


from IPython.nbconvert.exporter.baseexporter import BaseExporter, ResourcesDict

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

#Jinja2 extensions to load.
JINJA_EXTENSIONS = ['jinja2.ext.loopcontrols']

default_filters = {
        'indent': indent,
        'markdown': filters.markdown2html,
        'ansi2html': filters.ansi2html,
        'filter_data_type': filters.DataTypeFilter,
        'get_lines': filters.get_lines,
        'highlight': filters.highlight,
        'highlight2html': filters.highlight,
        'highlight2latex': filters.highlight2latex,
        'markdown2latex': filters.markdown2latex,
        'markdown2rst': filters.markdown2rst,
        'pycomment': filters.python_comment,
        'rm_ansi': filters.remove_ansi,
        'rm_dollars': filters.strip_dollars,
        'rm_fake': filters.rm_fake,
        'html_text' : filters.html_text,
        'add_anchor': filters.add_anchor,
        'ansi2latex': filters.ansi2latex,
        'rm_math_space': filters.rm_math_space,
        'wrap': filters.wrap
}

#-----------------------------------------------------------------------------
# Class
#-----------------------------------------------------------------------------

class Exporter(BaseExporter):
    """
    Exports notebooks into other file formats.  Uses Jinja 2 templating engine
    to output new formats.  Inherit from this class if you are creating a new
    template type along with new filters/transformers.  If the filters/
    transformers provided by default suffice, there is no need to inherit from
    this class.  Instead, override the template_file and file_extension
    traits via a config file.
    
    {filters}
    """
    
    # finish the docstring
    __doc__ = __doc__.format(filters = '- '+'\n    - '.join(default_filters.keys()))


    template_file = Unicode(
            '', config=True,
            help="Name of the template file to use")

    file_extension = Unicode(
        'txt', config=True, 
        help="Extension of the file that should be written to disk"
        )

    template_path = Unicode(
        os.path.join("..", "templates"), config=True,
        help="Path where the template files are located.")

    template_skeleton_path = Unicode(
        os.path.join("..", "templates", "skeleton"), config=True,
        help="Path where the template skeleton files are located.") 

    #Jinja block definitions
    jinja_comment_block_start = Unicode("", config=True)
    jinja_comment_block_end = Unicode("", config=True)
    jinja_variable_block_start = Unicode("", config=True)
    jinja_variable_block_end = Unicode("", config=True)
    jinja_logic_block_start = Unicode("", config=True)
    jinja_logic_block_end = Unicode("", config=True)
    
    #Extension that the template files use.    
    template_extension = Unicode(".tpl", config=True)


    filters = Dict(config=True,
        help="""Dictionary of filters, by name and namespace, to add to the Jinja
        environment.""")


    def __init__(self, config=None, extra_loaders=None, **kw):
        """
        Public constructor
    
        Parameters
        ----------
        config : config
            User configuration instance.
        extra_loaders : list[of Jinja Loaders]
            ordered list of Jinja loder to find templates. Will be tried in order
            before the default FileSysteme ones.
        """
        
        #Call the base class constructor
        c = self.default_config
        if config:
            c.merge(config)

        super(Exporter, self).__init__(config=c, **kw)

        #Init
        self._init_environment(extra_loaders=extra_loaders)
        self._init_filters()


    def from_notebook_node(self, nb, resources=None, **kw):
        """
        Convert a notebook from a notebook node instance.
    
        Parameters
        ----------
        nb : Notebook node
        resources : dict (**kw) 
            of additional resources that can be accessed read/write by 
            transformers and filters.
        """

        #Preprocess
        nb_copy, resources = super(BaseExporter, self).from_notebook_node(nb, resources=None, **kw)

        #Convert
        self.template = self.environment.get_template(self.template_file + self.template_extension)
        output = self.template.render(nb=nb_copy, resources=resources)
        return output, resources


    def register_filter(self, name, jinja_filter):
        """
        Register a filter.
        A filter is a function that accepts and acts on one string.  
        The filters are accesible within the Jinja templating engine.
    
        Parameters
        ----------
        name : str
            name to give the filter in the Jinja engine
        filter : filter
        """
        if jinja_filter is None:
            raise TypeError('filter')
        isclass = isinstance(jinja_filter, type)
        constructed = not isclass

        #Handle filter's registration based on it's type
        if constructed and isinstance(jinja_filter, py3compat.string_types):
            #filter is a string, import the namespace and recursively call
            #this register_filter method
            filter_cls = import_item(jinja_filter)
            return self.register_filter(name, filter_cls)
        
        if constructed and hasattr(jinja_filter, '__call__'):
            #filter is a function, no need to construct it.
            self.environment.filters[name] = jinja_filter
            return jinja_filter

        elif isclass and isinstance(jinja_filter, MetaHasTraits):
            #filter is configurable.  Make sure to pass in new default for 
            #the enabled flag if one was specified.
            filter_instance = jinja_filter(parent=self)
            self.register_filter(name, filter_instance )

        elif isclass:
            #filter is not configurable, construct it
            filter_instance = jinja_filter()
            self.register_filter(name, filter_instance)

        else:
            #filter is an instance of something without a __call__ 
            #attribute.  
            raise TypeError('filter')

        
    def _init_environment(self, extra_loaders=None):
        """
        Create the Jinja templating environment.
        """
        here = os.path.dirname(os.path.realpath(__file__))
        loaders = []
        if extra_loaders:
            loaders.extend(extra_loaders)

        loaders.append(FileSystemLoader([
                os.path.join(here, self.template_path),
                os.path.join(here, self.template_skeleton_path),
                ]))

        self.environment = Environment(
            loader= ChoiceLoader(loaders),
            extensions=JINJA_EXTENSIONS
            )
        
        #Set special Jinja2 syntax that will not conflict with latex.
        if self.jinja_logic_block_start:
            self.environment.block_start_string = self.jinja_logic_block_start
        if self.jinja_logic_block_end:
            self.environment.block_end_string = self.jinja_logic_block_end
        if self.jinja_variable_block_start:
            self.environment.variable_start_string = self.jinja_variable_block_start
        if self.jinja_variable_block_end:
            self.environment.variable_end_string = self.jinja_variable_block_end
        if self.jinja_comment_block_start:
            self.environment.comment_start_string = self.jinja_comment_block_start
        if self.jinja_comment_block_end:
            self.environment.comment_end_string = self.jinja_comment_block_end

    
    def _init_filters(self):
        """
        Register all of the filters required for the exporter.
        """
        
        #Add default filters to the Jinja2 environment
        for key, value in default_filters.items():
            self.register_filter(key, value)

        #Load user filters.  Overwrite existing filters if need be.
        if self.filters:
            for key, user_filter in self.filters.items():
                self.register_filter(key, user_filter)


    def _init_resources(self, resources):
        

        resources = super(Exporter, self)._init_resources(resources)

        if 'metadata' in resources:
            if not isinstance(resources['metadata'], ResourcesDict):
                resources['metadata'] = ResourcesDict(resources['metadata'])
        else:
            resources['metadata'] = ResourcesDict()
            if not resources['metadata']['name']: 
                resources['metadata']['name'] = 'Notebook'

        #Set the output extension
        resources['output_extension'] = self.file_extension
        return resources
