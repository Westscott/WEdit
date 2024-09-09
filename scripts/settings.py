import os
import pygments.lexers
import pygments.lexers.dotnet

global _selected_syntax
_selected_syntax = "txt"
global syntaxOptions
syntaxOptions = {
    "txt": pygments.lexers.TextLexer,
    "py": pygments.lexers.PythonLexer,
    "c#": pygments.lexers.CSharpLexer,
    "perl": pygments.lexers.PerlLexer,
    "html": pygments.lexers.HtmlLexer,
    "cpp": pygments.lexers.CppLexer,
    "java": pygments.lexers.JavaLexer
}

global _fontSize
_fontSize = 14
global _selected_typeface
_selected_typeface = "Terminal"
global typefaceOptions
typefaceOptions = {
    "Segoe UI": 1,
    "Courier New": 2,
    "Consolas": 3,
    "Arial": 4,
    "Trebuchet MS": 5,
    "Terminal": 6
}

# use YAML files and make an index of custom themes
global _selected_colorscheme
_selected_colorscheme = "monokai"
global _colorscheme_index
_colorscheme_index = 0
global colorschemeOptions
colorschemeOptions = {
    0: "monokai",
    1: "mariana",
    #2: "hacker",
    2: "dracula",
    3: "ayu-light",
    4: "ayu-dark"
}



#! Setup Propper Theme
global backgroundOptions
backgroundOptions = [
    "#282923",
    "#343d46",
    "#282a36",
    "#fafafa",
    "#0a0e14"
]
global fontColorOptions
fontColorOptions = [
    "#f8f8f2",
    "#d8dee9",
    "#f8f8f2",
    "#000000",
    "#f8f8f2"
]
global highlightColorOptions
highlightColorOptions = [
    "#717378",
    "#717378",
    "#717378",
    "#717378",
    "#717378"
]



global pythonKeywordList
pythonKeywordList = [
    "False", "None", "True", "and", "as", "assert", "async", "await", "break", "class", "continue", "def", "del", "elif", "else", "except", "finally", "for", "from", "global", "if", "import", "in", "is", "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try", "while", "with", "yield"
]