
import PyInstaller.__main__
options = [
    '--onefile',
    '--strip',
    '--windowed',
    '--noconsole',
    #'--icon=icon.ico',
    'main.pyw'
]
PyInstaller.__main__.run(options)
