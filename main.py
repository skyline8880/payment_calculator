import calendar
import datetime as dt
import os
import sys

from kivy.animation import Animation
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

custom_img = resource_path('debt.png')
custom_icon = resource_path('debt_ico.ico')

class DebtCounterApp(MDApp):
    def change_type(self):
        if self.state == 0:
            self.state = 1
            self.toolbar.title = ("қарзи аннуитетӣ").upper()
        else:
            self.state = 0
            self.toolbar.title = ("қарзи дифференсиалӣ").upper()

    def calculate(self, args=None, kwargs=None):
        if (self.loan_input.text == '' or self.terms_input.text == '' or self.interest_input.text == ''):
            self.outro_anim(self.payment_per_month)
            self.outro_anim2(self.interest_a_day)
            self.outro_anim3(self.interest_hole_period)
            self.outro_anim4(self.payment_hole_period)

        try:
            loan = int(self.loan_input.text)
            terms = int(self.terms_input.text)
            interest = float(self.interest_input.text)
            today = dt.datetime.today()
            num_of_days_in_month = int(calendar.monthrange(today.year, today.month)[1])
            if self.toolbar.title == ("қарзи аннуитетӣ").upper():
                interest_per_month = interest / (100*12)
                annuity_payment = round(float(
                    loan * ((interest_per_month *
                             ((1 + interest_per_month) ** terms)) /
                             (((1 + interest_per_month) ** terms) - 1))), 2)
                self.payment_per_month.text = str(annuity_payment)
                self.interest_a_day.text = str(
                    round(((interest_per_month / num_of_days_in_month) * loan), 2))
                self.interest_hole_period.text = str(
                    round(((annuity_payment * terms) - loan), 2)
                )
                self.payment_hole_period.text = str(
                    round((annuity_payment * terms), 2)
                )
                self.intro_anim(self.payment_per_month)
                self.intro_anim2(self.interest_a_day)
                self.intro_anim3(self.interest_hole_period)
                self.intro_anim4(self.payment_hole_period)
            else:
                loan_per_month = loan / terms
                interest_per_month = (loan * (interest/100) * num_of_days_in_month) / 365
                self.payment_per_month.text = str(
                    round(float(loan_per_month + interest_per_month), 2))
                self.interest_a_day.text = str(
                    round((interest_per_month / num_of_days_in_month), 2))
                list_of_payments = []
                month_counter = 0
                loan_cut = 0
                month = dt.datetime.today().month
                year = dt.datetime.today().year
                for _ in range(terms):
                    next_month = month + month_counter
                    if next_month == 13:
                        year += 1
                        next_month = 1
                        month = 1
                        month_counter = 0
                    days_in_current_month = int(calendar.monthrange(year, next_month)[1])
                    current_payment = round((
                        (((loan - loan_cut) * (interest/100) * days_in_current_month) / 365) + loan_per_month), 
                        2)
                    list_of_payments.append(current_payment)
                    loan_cut += loan_per_month
                    month_counter += 1
                self.interest_hole_period.text = str(
                    round((sum(list_of_payments) - loan), 2))
                self.payment_hole_period.text = str(
                    round((sum(list_of_payments)), 2))
                self.intro_anim(self.payment_per_month)
                self.intro_anim2(self.interest_a_day)
                self.intro_anim3(self.interest_hole_period)
                self.intro_anim4(self.payment_hole_period)
        except:
            return

    def intro_anim(self, widget):
        anim = Animation(pos_hint={'center_x': 0.5  }, duration=.30)
        anim.start(widget)

    def intro_anim2(self, widget):
        anim = Animation(pos_hint={'center_x': 0.5  }, duration=.35)
        anim.start(widget)

    def intro_anim3(self, widget):
        anim = Animation(pos_hint={'center_x': 0.5  }, duration=.40)
        anim.start(widget)

    def intro_anim4(self, widget):
        anim = Animation(pos_hint={'center_x': 0.5  }, duration=.45)
        anim.start(widget)
    
    def outro_anim(self, widget):
        anim = Animation(pos_hint={'center_x': -1  }, duration=.35)
        anim.start(widget)

    def outro_anim2(self, widget):
        anim = Animation(pos_hint={'center_x': -1  }, duration=.40)
        anim.start(widget)

    def outro_anim3(self, widget):
        anim = Animation(pos_hint={'center_x': -1  }, duration=.45)
        anim.start(widget)

    def outro_anim4(self, widget):
        anim = Animation(pos_hint={'center_x': -1  }, duration=.50)
        anim.start(widget)

    def build(self):
        self.title = 'Ҳисобкунаки пардохт'
        self.icon = custom_img
        self.state = 1
        self.theme_cls.primary_palette = "Cyan"
        self.screen = MDScreen()
        self.toolbar = MDTopAppBar(
            title=("қарзи аннуитетӣ").upper(),
            md_bg_color=(0, 20, 21.2, 0.8),
            opposite_colors=True
            )
        self.toolbar.pos_hint = {"top": .999}
        self.toolbar.right_action_items = [
            ["rotate-3d-variant", lambda x: (self.change_type(), self.calculate())]]
        
        self.screen.add_widget(self.toolbar)

        self.loan_input = MDTextField(
            hint_text="маблағи қарз",
            input_filter="int",
            write_tab=False,
            multiline=False,
            halign="right",
            size_hint=(0.3, 1),
            pos_hint={"center_x": 0.5, "center_y":0.82},
            font_size=18,
        )
        self.loan_input.bind(text=self.calculate)
        self.terms_input = MDTextField(
            hint_text="мӯҳлати қарз",
            input_filter="int",
            write_tab=False,
            multiline=False,
            halign="right",
            size_hint=(0.3, 1),
            pos_hint={"center_x": 0.5, "center_y":0.75},
            font_size=18,
        )
        self.terms_input.bind(text=self.calculate)
        self.interest_input = MDTextField(
            hint_text="фоизи солонаи қарз",
            input_filter="float",
            write_tab=False,
            multiline=False,
            halign="right",
            size_hint=(0.3, 1),
            pos_hint={"center_x": 0.5, "center_y":0.68},
            font_size=18,
        )
        self.interest_input.bind(text=self.calculate)

        self.screen.add_widget(self.loan_input)
        self.screen.add_widget(self.terms_input)
        self.screen.add_widget(self.interest_input)

        self.payment_per_month = MDTextField(
            readonly=True,
            hint_text="пардохти моҳона",
            halign="right",
            size_hint=(0.3, 1),
            pos_hint={"center_x": -1, "center_y": 0.56},
            font_size=18
        )
        self.interest_a_day = MDTextField(
            readonly=True,
            hint_text="пардохти фоизҳо дар як руз",
            halign="right",
            size_hint=(0.3, 1),
            pos_hint={"center_x": -1, "center_y": 0.49},
            font_size=18
        )
        self.interest_hole_period = MDTextField(
            readonly=True,
            hint_text="пардохти фоизҳо барои тамоми муҳлат",
            halign="right",
            size_hint=(0.3, 1),
            pos_hint={"center_x": -1, "center_y": 0.42},
            font_size=18
        )
        self.payment_hole_period = MDTextField(
            readonly=True,
            hint_text="пардохтҳои пурраи муҳлат",
            halign="right",
            size_hint=(0.3, 1),
            pos_hint={"center_x": -1, "center_y": 0.35},
            font_size=18
        )

        self.screen.add_widget(self.payment_per_month)
        self.screen.add_widget(self.interest_a_day)
        self.screen.add_widget(self.interest_hole_period)
        self.screen.add_widget(self.payment_hole_period)
        return self.screen


if __name__ == '__main__':
    DebtCounterApp().run()
