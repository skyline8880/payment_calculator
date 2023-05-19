import locale

from kivy.clock import Clock
from kivymd.uix.textfield import MDTextField

locale.setlocale(locale.LC_ALL, '')


class LoanValueInput(MDTextField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_filter = "int"
        self.halign = "left"
        self.write_tab = False
        self.multiline = False
        self.helper_text_mode = "persistent"
        self.selection_text = "readonly"

    def delete_selection(self, from_undo=False):
        return

    def do_backspace(self, from_undo=False, mode='bkspc'):
        if self.text != "":
            if len(self.text) != 1:
                z = "".join(self.text[:-1].split())
                self.text = f"{int(z):n}"
            else:
                self.text = ""

    def insert_text(self, substring, from_undo = False):
        if not substring.isdigit():
            return
        cursor_column, cusror_row = self.cursor
        text = self._lines[cusror_row]
        t = text[:cursor_column] + substring + text[cursor_column:]
        t = "".join(t.split())
        x = f"{int(t):n}"
        if len(x) == 26:
            return
        elif str(x).startswith('0'):
            return
        super().insert_text(substring, from_undo = from_undo)
        self._set_line_text(cusror_row, x)
        Clock.schedule_once(lambda dt : setattr(
                self, "cursor", (cursor_column + 2, cusror_row)))


class TermsValueInput(MDTextField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_filter = "int"
        self.halign = "left"
        self.write_tab = False
        self.multiline = False
        self.helper_text_mode = "persistent"

    def delete_selection(self, from_undo=False):
        return

    def do_backspace(self, from_undo=False, mode='bkspc'):
        if self.text != "":
            self.text = self.text[:-1]

    def insert_text(self, substring, from_undo = False):
        if not substring.isdigit():
            return
        cursor_column, cusror_row = self.cursor
        text = self._lines[cusror_row]
        t = text[:cursor_column] + substring + text[cursor_column:]
        if len(t) == 5:
            return
        elif str(t).startswith('0'):
            return
        super().insert_text(substring, from_undo = from_undo)
        self._set_line_text(cusror_row, t)
        Clock.schedule_once(lambda dt : setattr(
                self, "cursor", (cursor_column + 2, cusror_row)))
                

class InterestValueInput(MDTextField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_filter = "float"
        self.halign = "left"
        self.write_tab = False
        self.multiline = False
        self.helper_text_mode = "persistent"
        if self.text == "0.":
            self.text = ""

    def on_focus(self, instance, value):
        if value:
            return
        else:
            if self.text == "0." or self.text == "0.0":
                self.text = ""

    def delete_selection(self, from_undo=False):
        return

    def do_backspace(self, from_undo=False, mode='bkspc'):
        if self.text != "":
            if self.text[-1] == "." and self.text[-2] == "0":
                self.text = ""
            else:
                self.text = self.text[:-1]
            
    def insert_text(self, substring, from_undo = False):
        if substring != ".":
            if not substring.isdigit():
                return
        cursor_column, cusror_row = self.cursor
        text = self._lines[cusror_row]
        if text[:cursor_column] == "" and substring == "0":
            substring = substring + "."
        if text[:cursor_column] == "" and substring == ".":
            return
        t = text[:cursor_column] + substring + text[cursor_column:]
        if t.count(".") == 2:
            return   
        if cursor_column == 3:
            if t[0] == "0" and t[1] == ".":
                if t[2] == "0" and t[3] == "0":
                    return
        if "." in t and len(t) == 5:
            return
        if not "." in t and len(t) == 4:
            return
        if float(t) > 100:
            return
        super().insert_text(substring, from_undo = from_undo)
        self._set_line_text(cusror_row, t)
        Clock.schedule_once(lambda dt : setattr(
                self, "cursor", (cursor_column + 2, cusror_row)))
        

class OutputValue(MDTextField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_filter = "float"
        self.halign = "left"
        self.write_tab = False
        self.multiline = False
        self.helper_text_mode = "persistent"
        self.readonly = True
