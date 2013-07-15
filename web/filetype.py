# Copyright (C) 2013  Matthieu Caneill <matthieu.caneill@gmail.com>
#
# This file is part of Debsources.
#
# Debsources is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import re

# Languages constants
(PYTHON, RUBY, PERL, PHP, SCALA, GO, XML, HTML, MARKDOWN, CSS, JSON,
JAVASCRIPT, COFFEESCRIPT, ACTIONSCRIPT, VBSCRIPT, LUA, JAVA, C, CPP, OBJECTIVEC,
VALA, CSHARP, D, SQL, LISP, CLOJURE, INI, APACHE, CMAKE, VHDL, DIFF, BASH,
TEX, BRAINFUCK, HASKELL, ERLANG, RUST, R) = range(38)

# Languages strings used by highlight.js
highlightjs = {
    PYTHON: "python",
    RUBY: "ruby",
    PERL: "perl",
    PHP: "php",
    SCALA: "scala",
    GO: "go",
    XML: "xml",
    HTML: "django",
    MARKDOWN: "markdown",
    CSS: "css",
    JSON: "json",
    JAVASCRIPT: "javascript",
    COFFEESCRIPT: "coffeescript",
    ACTIONSCRIPT: "actionscript",
    VBSCRIPT: "vbscript",
    LUA: "lua",
    JAVA: "java",
    C: "cpp",
    CPP: "cpp",
    OBJECTIVEC: "objectivec",
    VALA: "vala",
    CSHARP: "cs",
    D: "d",
    SQL: "sql",
    LISP: "lisp",
    CLOJURE: "clojure",
    INI: "ini",
    APACHE: "apache",
    CMAKE: "cmake",
    VHDL: "vhdl",
    DIFF: "diff",
    BASH: "bash",
    TEX: "tex",
    BRAINFUCK: "brainfuck",
    HASKELL: "haskell",
    ERLANG: "erlang",
    RUST: "rust",
    R: "r",
    }

# Filename regexes
filename_regexes = [
    (PYTHON, [r'\.py$']),
    (RUBY, [r'\.rb$']),
    (PERL, [r'\.pl$', r'\.PL', r'\.pm$', r'\.PM']),
    (PHP, [r'\.php$']),
    (SCALA, [r'\.scala$']),
    (GO, [r'\.go$']),
    (XML, [r'\.xml$']),
    (HTML, [r'\.htm$', r'\.html$']),
    (MARKDOWN, [r'\.md$']),
    (CSS, [r'\.css$']),
    (JSON, [r'\.json$']),
    (JAVASCRIPT, [r'\.js$']),
    (COFFEESCRIPT, [r'\.coffee$']),
    (ACTIONSCRIPT, [r'\.as$']),
    (VBSCRIPT, [r'\.vbs$']),
    (LUA, [r'\.lua$']),
    (JAVA, [r'\.java$']),
    (C, [r'\.h$', r'\.c$', r'\.C$', r'\.cc$']),
    (CPP, [ r'\.cpp$', r'\.hpp$']),
    (OBJECTIVEC, [r'\.m$']),
    (VALA, [r'\.vala$', r'\.api$']),
    (CSHARP, [r'\.cs$']),
    (D, [r'\.d$']),
    (SQL, [r'\.sql$']),
    (LISP, [r'\.lisp$', r'\.el$']),
    (CLOJURE, [r'\.clj$']),
    (INI, [r'\.ini$']),
    (APACHE, [r'apache.conf$']),
    (CMAKE, [r'CMakeLists\.txt$']),
    (VHDL, [r'\.vhd$', r'\.vhdl$']),
    (DIFF, [r'\.patch$', r'\.diff$']),
    (BASH, [r'\.sh$']),
    (TEX, [r'\.tex$']),
    (BRAINFUCK, [r'\.bf$']),
    (HASKELL, [r'\.hs$', r'\.lhs$']),
    (ERLANG, [r'\.erl$']),
    (RUST, [r'\.rs$']),
    (R, ['\.r$']),
    ]

# Shebang map:
# from http://git.geany.org/geany/tree/src/filetypes.c?h=1.23#n910
shebangs = dict(
    sh =	BASH,
    bash =	BASH,
    dash =	BASH,
    perl =	PERL,
    python =	PYTHON,
    php =	PHP,
    ruby =	RUBY,
    #tcl =	TCL,
    make =	CMAKE,
    zsh =	BASH,
    ksh =	BASH,
    csh =	BASH,
    ash =	BASH,
    dmd =	D,
    #wish =	TCL,
    )

def get_filetype(filename, firstline):
    """
    Tries to guess the programming language used in the file.
    
    It firsts looks at the first line, if it's a shebang:
    #!/usr/bin/env foo
    
    And if it's not successful it looks at the filename.
    """
    filetype = get_filetype_from_firstline(firstline)
    if filetype is None:
        filetype = get_filetype_from_filename(filename)
    
    return filetype

def get_filetype_from_firstline(firstline):
    """
    Tries to guess the language with the first line of a file.
    Looks for a shebang, or html/xml/php typical begin tags.
    """
    # we check if it's a shebang:
    if firstline.startswith("#!"):
        # we get the last part:
        interp = firstline.split("/")[-1]
        if interp.startswith("env"): # shebang type: #!/usr/bin/env foo
            interp = interp.split()[-1]
        else: # shebang type: #!/usr/bin/foo
            pass
        if interp in shebangs.keys():
            return shebangs[interp]
        else:
            return None
    
    elif (firstline.lower().startswith("<html")
          or firstline.lower().startswith("<!doctype html")):
        return HTML
    
    elif firstline.lower().startswith("<?xml"):
        return XML
    
    elif firstline.lower().startswith("<?php"):
        return PHP
    
    else:
        return None

def get_filetype_from_filename(filename):
    """
    Ties to guess the language with the filename (and the regexes table).
    """
    for language, patternslist in filename_regexes:
        for pattern in patternslist:
            if re.search(pattern, filename):
                return language
    return None

def get_highlightjs_language(filename, firstline):
    """
    Returns the highligth.js string corresponding to a language
    (used for syntactic code coloration).
    """
    firstline = firstline.rstrip()
    language = get_filetype(filename, firstline)
    if language is None or language not in highlightjs.keys():
        return None
    else:
        return highlightjs[language]


if __name__ == "__main__":
    assert get_filetype("foo", "#!/usr/bin/env python") == PYTHON
    assert get_filetype("foo", "#!/usr/bin/python") == PYTHON
    assert get_filetype("foo.py", "foobar") == PYTHON
    
    assert get_filetype("foo", "<html><head>") == HTML
    assert get_filetype("foo", "<?xml>") == XML
    assert get_filetype("foo", "<?php echo('hello') ?>") == PHP
    
    assert get_filetype("foo", "#!/usr/bin/env ruby") == RUBY
    assert get_filetype("foo.rb", "foobar") == RUBY
    
    assert get_highlightjs_language("foo.html", "foobar") == "django"
    assert get_highlightjs_language("foo", "#!/bin/perl\n") == "perl"
    
    assert get_filetype("foo", "foobar") is None