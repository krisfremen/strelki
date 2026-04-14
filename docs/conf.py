# -- Path setup --------------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.abspath(".."))
import strelki

# -- Project information -----------------------------------------------------

project = "Strelki"
copyright = "2023, Chris Smith"
author = "Chris Smith"

release = strelki.__version__

# -- General configuration ---------------------------------------------------

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx_autodoc_typehints",
    "sphinx_rtd_theme",
]

templates_path = []

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

master_doc = "index"
source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}
pygments_style = "sphinx"

language = "en"

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_theme_path = []
html_static_path = []

html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = True

html_context = {
    "display_github": True,
    "github_user": "krisfremen",
    "github_repo": "strelki",
    "github_version": "master/docs/",
}

# https://sphinx-rtd-theme.readthedocs.io/en/stable/index.html
html_theme_options = {
    "logo_only": False,
    "prev_next_buttons_location": "both",
    "style_nav_header_background": "grey",
    # TOC options
    "collapse_navigation": False,
    "navigation_depth": 3,
}

# Generate PDFs with unicode characters
# https://docs.readthedocs.io/en/stable/guides/pdf-non-ascii-languages.html
latex_engine = "xelatex"
