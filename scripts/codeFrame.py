import settings as WDTS
from westchlor import CodeView


def CallCV(mainFrame):
    _cvMain = CodeView(
        mainFrame,
        lexer=WDTS.syntaxOptions[WDTS._selected_syntax],
        color_scheme=WDTS._selected_colorscheme,
        font=(WDTS._selected_typeface, WDTS._fontSize),
        linenums_border=0,
        default_context_menu=True,
     )
    #? -12 for single line 
    #_cvMain._line_numbers.configure(borderwidth=0)
    return _cvMain