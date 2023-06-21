# payment_calculator

App for calculating loan payment by type

### create virtual environment

```bash
python -m venv venv
```

make shure your environment is activated

### requirements

use [pip] (https://pip.pypa.io/en/stable/) to install requirements
```bash
pip install -r requirements.txt
```

### packaging using pyinstaller

write command below in terminal

```bash
--onefile --windowed --add-data 'debt.png' --icon=debt_ico.ico main.py
```

### specify main.spec file
add imports in the first row in ```main.spec``` file:
* ```python
    from kivy_deps import sdl2, glew
    ```
add data in coll:
* ```python
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)]
    ```
### make changes in ```__init__.py```
get to venv\Lib\site-packages\kivymd find ```__init__.py``` file and add 2 imports:
* ```python 
    import kivymd.icon_definitions # NOQA```
* ```python
    import kivymd.uix.card # NOQA```