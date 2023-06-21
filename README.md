# payment_calculator
App for calculating loan payment by type
## packaging using pyinstaller
--onefile --windowed --add-data 'debt.png' --icon=debt_ico.ico main.py
### specify main.spec file
add imports in the highes row in main.spec file:
* from kivy_deps import sdl2, glew
add data in coll:
* *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)]
### make changes in __init__.py
get to venv\Lib\site-packages\kivymd\__init__.py and add 2 imports:
* import kivymd.icon_definitions # NOQA
* import kivymd.uix.card # NOQA
above: from kivymd.tools.packaging.pyinstaller import hooks_path  # NOQA