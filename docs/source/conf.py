# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'MMDS'
copyright = '2026, John Aoga'
author = 'John Aoga'

release = '0.1'
version = '0.1.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'myst_parser',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# The quiz_issues/*.md files are the source question bank for
# scripts/generate_quizzes.py, not documentation pages.
exclude_patterns = ['part6/quiz_issues/**']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Custom static files (interactive QCM)
html_static_path = ['_static']
html_css_files = ['quiz.css']
html_js_files = ['quiz.js']

# -- Options for EPUB output
epub_show_urls = 'footnote'

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}
