# -*- coding: utf-8 -*-
#
# libpysal documentation build configuration file, created by
# sphinx-quickstart on Wed Jun  6 15:54:22 2018.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import sphinx_bootstrap_theme
import libpysal


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [  #'sphinx_gallery.gen_gallery',
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinxcontrib.bibtex",
    "sphinx.ext.mathjax",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "numpydoc",
    #'sphinx.ext.napoleon',
    "matplotlib.sphinxext.plot_directive",
    "nbsphinx",
]
bibtex_bibfiles = ["_static/references.bib"]

# sphinx_gallery_conf = {
#      # path to your examples scripts
#      'examples_dirs': '../examples',
#      # path where to save gallery generated examples
#      'gallery_dirs': 'auto_examples',
#      'backreferences_dir': False,
# }


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "libpysal"
copyright = "2018-, pysal developers"
author = "pysal developers"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The full version.
version = libpysal.__version__
release = libpysal.__version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "tests/*"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

# html_theme = 'alabaster'
html_theme = "bootstrap"
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
html_title = "%s v%s Manual" % (project, version)

# (Optional) Logo. Should be small enough to fit the navbar (ideally 24x24).
# Path should be relative to the ``_static`` files directory.
# html_logo = "_static/images/CGS_logo.jpg"
# html_logo = "_static/images/CGS_logo_green.png"
# html_logo = "_static/images/pysal_logo_small.jpg"
html_favicon = "_static/images/pysal_favicon.ico"


# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    # Navigation bar title. (Default: ``project`` value)
    "navbar_title": project,
    # Render the next and previous page links in navbar. (Default: true)
    "navbar_sidebarrel": False,
    # Render the current pages TOC in the navbar. (Default: true)
    #'navbar_pagenav': True,
    #'navbar_pagenav': False,
    # No sidebar
    "nosidebar": True,
    # Tab name for the current pages TOC. (Default: "Page")
    #'navbar_pagenav_name': "Page",
    # Global TOC depth for "site" navbar tab. (Default: 1)
    # Switching to -1 shows all levels.
    "globaltoc_depth": 2,
    # Include hidden TOCs in Site navbar?
    #
    # Note: If this is "false", you cannot have mixed ``:hidden:`` and
    # non-hidden ``toctree`` directives in the same page, or else the build
    # will break.
    #
    # Values: "true" (default) or "false"
    "globaltoc_includehidden": "true",
    # HTML navbar class (Default: "navbar") to attach to <div> element.
    # For black navbar, do "navbar navbar-inverse"
    #'navbar_class': "navbar navbar-inverse",
    # Fix navigation bar to top of page?
    # Values: "true" (default) or "false"
    "navbar_fixed_top": "true",
    # Location of link to source.
    # Options are "nav" (default), "footer" or anything else to exclude.
    "source_link_position": "footer",
    # Bootswatch (http://bootswatch.com/) theme.
    #
    # Options are nothing (default) or the name of a valid theme
    # such as "amelia" or "cosmo", "yeti", "flatly".
    "bootswatch_theme": "yeti",
    # Choose Bootstrap version.
    # Values: "3" (default) or "2" (in quotes)
    "bootstrap_version": "3",
    "navbar_links": [
        # ("Gallery", "auto_examples/index"),
        ("Installation", "installation"),
        ("User Guide", "user-guide/intro"),
        ("API", "api"),
        ("References", "references"),
    ],
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}
# html_sidebars = {'sidebar': ['localtoc.html', 'sourcelink.html', 'searchbox.html']}

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "%sdoc" % project


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "%s.tex" % project,
        "%s Documentation" % project,
        "pysal developers",
        "manual",
    ),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, project, "%s Documentation" % project, [author], 1)]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        project,
        "%s Documentation" % project,
        author,
        project,
        "One line description of project.",
        "Miscellaneous",
    ),
]

# -----------------------------------------------------------------------------
# Napoleon configuration
# -----------------------------------------------------------------------------
# numpydoc_show_class_members = True
# numpydoc_class_members_toctree = False
#
# napoleon_use_ivar = True

# -----------------------------------------------------------------------------
# Autosummary
# -----------------------------------------------------------------------------

# Generate the API documentation when building
autosummary_generate = True

# avoid showing members twice
numpydoc_show_class_members = False
numpydoc_use_plots = True
class_members_toctree = True

#
numpydoc_show_inherited_class_members = True
numpydoc_xref_param_type = True

# automatically document class members
autodoc_default_options = {"members": True, "undoc-members": True}

# display the source code for Plot directive
plot_include_source = True


def setup(app):
    app.add_css_file("pysal-styles.css")


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "geopandas": ("https://geopandas.org/en/latest/", None),
    "libpysal": ("https://pysal.org/libpysal/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
    "networkx": ("https://networkx.org/documentation/stable/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "python": ("https://docs.python.org/3.12/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
}


# This is processed by Jinja2 and inserted before each notebook
nbsphinx_prolog = r"""
{% set docname = env.doc2path(env.docname, base=None) %}

.. only:: html

    .. role:: raw-html(raw)
        :format: html

    .. nbinfo::

        This page was generated from `{{ docname }}`__.
        Interactive online version:
        :raw-html:`<a href="https://mybinder.org/v2/gh/pysal/libpysal/master?filepath={{ docname }}"><img alt="Binder badge" src="https://mybinder.org/badge_logo.svg" style="vertical-align:text-bottom"></a>`

    __ https://github.com/pysal/libpysal/blob/master/{{ docname }}

.. raw:: latex

    \nbsphinxstartnotebook{\scriptsize\noindent\strut
    \textcolor{gray}{The following section was generated from
    \sphinxcode{\sphinxupquote{\strut {{ docname | escape_latex }}}} \dotfill}}
"""

# This is processed by Jinja2 and inserted after each notebook
nbsphinx_epilog = r"""
.. raw:: latex

    \nbsphinxstopnotebook{\scriptsize\noindent\strut
    \textcolor{gray}{\dotfill\ \sphinxcode{\sphinxupquote{\strut
    {{ env.doc2path(env.docname, base='doc') | escape_latex }}}} ends here.}}
"""

# List of arguments to be passed to the kernel that executes the notebooks:
nbsphinx_execute_arguments = [
    "--InlineBackend.figure_formats={'svg', 'pdf'}",
    "--InlineBackend.rc={'figure.dpi': 96}",
]

mathjax3_config = {
    "TeX": {"equationNumbers": {"autoNumber": "AMS", "useLabelIds": True}},
}
