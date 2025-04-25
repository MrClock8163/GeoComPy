import os
import sys
sys.path.insert(0, os.path.abspath("../src"))

project = "GeoComPy"
copyright = "2025, MrClock8163"
author = "MrClock8163"

# from geocompy._version import __version__
# release = version = "0.0.1"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.doctest",
    "sphinx.ext.linkcode",
    "sphinx.ext.napoleon",
    "notfound.extension",
    "sphinx_last_updated_by_git",
    "sphinx_immaterial"
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "serial": ("https://pyserial.readthedocs.io/en/latest/", None)
}

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
templates_path = ["_templates"]

html_static_path = ["_static"]
html_css_files = [
    "css/custom.css",
]
html_logo = "_static/logo.svg"
html_favicon = "_static/favicon.svg"
html_last_updated_fmt = "%d %b %Y"
html_copy_source = False
html_scaled_image_link = False
html_use_opensearch = "https://geocompy.readthedocs.io"
html_theme = 'sphinx_immaterial'
html_theme_options = {
    "icon": {
        "repo": "fontawesome/brands/github",
        "edit": "material/file-edit-outline",
    },
    "features": [
        "content.code.copy",
        "navigation.top",
        "navigation.sections",
        "navigation.expand",
        "navigation.path",
        "toc.follow"
    ],
    "site_url": "https://geocompy.readthedocs.io",
    "repo_url": "https://github.com/MrClock8163/geocompy",
    "repo_name": "GeoComPy",
    "palette": [
        {
            "media": "(prefers-color-scheme)",
            "toggle": {
                "icon": "material/brightness-auto",
                "name": "Switch to light mode",
            },
        },
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "custom",
            "accent": "custom",
            "toggle": {
                "icon": "material/weather-sunny",
                "name": "Switch to dark mode",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "custom",
            "accent": "custom",
            "toggle": {
                "icon": "material/weather-night",
                "name": "Switch to system preference",
            },
        },
    ],
    "social": [
        {
            "icon": "fontawesome/brands/github",
            "link": "https://github.com/MrClock8163/geocompy",
            "name": "Project on GitHub"
        },
        {
            "icon": "fontawesome/brands/python",
            "link": "https://pypi.org/project/geocompy/",
        }
    ],
    "version_dropdown": True,
}

# Immaterial toc adjustments
object_description_options = [
    (
        "py:.*",
        {
            "include_fields_in_toc": False,
            "include_rubrics_in_toc": False
        }
    ),
    (
        "py:parameter",
        {
            "include_in_toc": False
        }
    )
]

autodoc_default_options = {
    "member-order": "groupwise",
    "no-show-inheritance": True,
    "members": True,
    "undoc-members": True
}
autoclass_content = "both"

napoleon_use_admonition_for_notes = True
napoleon_preprocess_types = True
napoleon_google_docstring = False
napoleon_use_ivar = True
napoleon_type_aliases = {
    "GeoComResponse": "~geocompy.protocols.GeoComResponse",
    "GsiOnlineResponse": "~geocompy.protocols.GsiOnlineResponse",
    "datetime": "~datetime.datetime"
}

python_display_short_literal_types = True
python_type_aliases = {
    "serial.serialwin32.Serial": "serial.Serial"
}

# Error checking
nitpicky = True
nitpick_ignore = {
    ("py:class", "optional"),
    ("py:param", "_E"),
    ("py:param", "_T")
}
nitpick_ignore_regex = {
    ("py:obj", r"[a-zA-Z]{3}\.\w+")
}


def linkcode_resolve(domain, info):  # GitHub source linking
    if domain != 'py':
        return None
    if not info['module']:
        return None
    filename = info['module'].replace('.', '/')
    return (
        "https://github.com/MrClock8163/"
        f"geocompy/tree/main/src/{filename:s}.py"
    )


latex_documents = [
    (
        "latexindex", "geocompy.tex",
        "GeoComPy documentation", "MrClock8163",
        "manual", False
    )
]
latex_logo = "geocompy_logo.png"
latex_elements = {
    "papersize": "a4paper",
    "extraclassoptions": "oneside",
    "makeindex": (
        r"\usepackage[columns=1]{idxlayout}"
        r"\makeindex"
    ),
    "preamble": (
        r"\usepackage{titlesec}"
        r"\newcommand{\sectionbreak}{\clearpage}"
    ),
    "fontpkg": (
        r"\usepackage{lmodern}"
        r"\renewcommand*{\familydefault}{\rmdefault}"
        r"\renewcommand{\ttdefault}{lmtt}"
    )
}
