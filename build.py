import PyInstaller.__main__ as pyi

pyinstaller_options = [
    "--name=RequestiPy",
    "--noconfirm",
    "--onefile",
    "--windowed",
    "--noconsole",
    "--icon=assets/icon.ico",
    "--add-data=assets/:assets/",
    "--add-data=venv/lib/pypy3.10/site-packages/customtkinter:customtkinter/",
    "--exclude-module=PyInstaller",
]

script_name = "main.py"

pyi.run(pyi_args=[str(script_name)] + pyinstaller_options)
