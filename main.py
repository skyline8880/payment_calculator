import calendar
import datetime as dt
import os
import sys
from decimal import Decimal

from kivy.animation import Animation
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar

from inputfields import (InterestValueInput, LoanValueInput, OutputValue,
                         TermsValueInput)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

custom_img = resource_path('debt.png')
custom_icon = resource_path('debt_ico.ico')


class DebtCounterApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def change_type(self):
        if self.state == 0:
            self.state = 1
            self.toolbar.title = self.appLanguage[self.lang]["annuity"]
        else:
            self.state = 0
            self.toolbar.title = self.appLanguage[self.lang]["differentiated"]

    def calculate(self, args=None, kwargs=None):
        if (self.loan_input.text == "" or self.terms_input.text == "" or self.interest_input.text == ""):
            self.outro_anim(self.payment_per_month)
            self.outro_anim2(self.interest_a_day)
            self.outro_anim3(self.interest_hole_period)
            self.outro_anim4(self.payment_hole_period)

        try:
            loan = int("".join(self.loan_input.text.split()))
            terms = int(self.terms_input.text)
            interest = float(self.interest_input.text)
            today = dt.datetime.today()
            num_of_days_in_month = int(calendar.monthrange(today.year, today.month)[1])
            if self.state == 1:
                interest_per_month = interest / (100*12)
                annuity_payment = round(float(
                    loan * ((interest_per_month *
                             ((1 + interest_per_month) ** terms)) /
                             (((1 + interest_per_month) ** terms) - 1))), 2)
                self.payment_per_month.text = str(
                    f"{(round(Decimal(annuity_payment), 2)):n}".replace(",", ".")
                    )
                self.interest_a_day.text = str(
                    f"{(round(Decimal((interest_per_month / num_of_days_in_month) * loan), 2)):n}".replace(",", ".")
                    )
                self.interest_hole_period.text = str(
                    f"{(round(Decimal((annuity_payment * terms) - loan), 2)):n}".replace(",", ".")
                )
                self.payment_hole_period.text = str(
                    f"{(round(Decimal(annuity_payment * terms), 2)):n}".replace(",", ".")
                )
                self.intro_anim(self.payment_per_month)
                self.intro_anim2(self.interest_a_day)
                self.intro_anim3(self.interest_hole_period)
                self.intro_anim4(self.payment_hole_period)
            else:
                loan_per_month = loan / terms
                interest_per_month = (loan * (interest/100) * num_of_days_in_month) / 365
                self.payment_per_month.text = str(
                    f"{(round(Decimal(loan_per_month + interest_per_month), 2)):n}".replace(",", ".")
                    )
                self.interest_a_day.text = str(
                    f"{(round(Decimal(interest_per_month / num_of_days_in_month), 2)):n}".replace(",", ".")
                    )
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
                    f"{(round(Decimal(sum(list_of_payments) - loan), 2)):n}".replace(",", ".")
                    )
                self.payment_hole_period.text = str(
                    f"{(round(Decimal(sum(list_of_payments)), 2)):n}".replace(",", ".")
                    )
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

    def clean_panel(self, *args):
        self.loan_input.text = ''
        self.terms_input.text = ''
        self.interest_input.text = ''

    def menu_open(self, instance):
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": i,
                "on_release": lambda x=i: self.menu_callback(x),
            } for i in self.list_items
        ]

        self.menu = MDDropdownMenu(
            caller=instance, 
            items=menu_items,
            width_mult=2,
        )
        self.menu.open()

    def menu_callback(self, text_item):
        self.lang = text_item
        self.title = self.appLanguage[self.lang]["appname"]
        if self.state == 1:
            self.toolbar.title = self.appLanguage[self.lang]["annuity"]
        else:
            self.toolbar.title = self.appLanguage[self.lang]["differentiated"]
        self.loan_input.helper_text = self.appLanguage[self.lang]["loanvalue"]
        self.terms_input.helper_text = self.appLanguage[self.lang]["terms"]
        self.interest_input.helper_text = self.appLanguage[self.lang]["interest"]
        self.payment_per_month.helper_text = self.appLanguage[self.lang]["monthlypayment"]
        self.interest_a_day.helper_text = self.appLanguage[self.lang]["interestday"]
        self.interest_hole_period.helper_text = self.appLanguage[self.lang]["interestperiod"]
        self.payment_hole_period.helper_text = self.appLanguage[self.lang]["paymentperiod"]
        self.menu.dismiss()

    def build(self):
        self.lang = "English"
        self.appLanguage = {
            "English": {
                "appname": "Payment calculator",
                "annuity": "Annuity loan",
                "differentiated": "Differentiated loan",
                "loanvalue": "Loan value",
                "terms": "Terms",
                "interest": "Interest",
                "monthlypayment": "Monthly payment",
                "interestday": "Interest per day",
                "interestperiod": "Interest at all period",
                "paymentperiod": "Payment at all period"
            },
            "Русский": {
                "appname": "Калькулятор платежей",
                "annuity": "Аннуитетный кредит",
                "differentiated": "Дифференцированный кредит",
                "loanvalue": "Сумма кредита",
                "terms": "Срок кредита",
                "interest": "Процентаная ставка",
                "monthlypayment": "Ежемесячный платёж",
                "interestday": "Сумма процента в день",
                "interestperiod": "Сумма процентов за весь период",
                "paymentperiod": "Сумма платежей за весь период"
            },
            "Тоҷикӣ": {
                "appname": "Ҳисобкунаки пардохт",
                "annuity": "Қарзи аннуитетӣ",
                "differentiated": "Қарзи дифференсиалӣ",
                "loanvalue": "Маблағи қарз",
                "terms": "Муҳлати қарз",
                "interest": "Фоизи солонаи қарз",
                "monthlypayment": "Пардохти моҳона",
                "interestday": "Пардохти фоизҳо дар як руз",
                "interestperiod": "Пардохти фоизҳо барои тамоми муҳлат",
                "paymentperiod": "Пардохтҳои пурраи муҳлат"
            }
        }

        self.title = self.appLanguage[self.lang]["appname"]
        self.icon = custom_img
        self.state = 1
        self.theme_cls.primary_palette = "Cyan"
        self.screen = MDScreen()
        self.toolbar = MDTopAppBar(
            title=self.appLanguage[self.lang]["annuity"],
            md_bg_color=(0, 20, 21.2, 0.8),
            opposite_colors=True
            )
        self.toolbar.pos_hint = {"top": .999}
        self.toolbar.right_action_items = [
            ["rotate-3d-variant", lambda x: (self.change_type(), self.calculate())],
            ["recycle", lambda x: self.clean_panel()],
            ["earth", lambda x: self.menu_open(x)]]
        
        self.screen.add_widget(self.toolbar)

        self.list_items = [
            "English", "Русский", "Тоҷикӣ"
        ]

        self.loan_input = LoanValueInput(
            helper_text=self.appLanguage[self.lang]["loanvalue"],
            size_hint=(0.3, 1),
            pos_hint={"center_x": 0.5, "center_y":0.82},
        )
        self.loan_input.bind(text=self.calculate)
        self.terms_input = TermsValueInput(
            helper_text=self.appLanguage[self.lang]["terms"],
            size_hint=(0.3, 1),
            pos_hint={"center_x": 0.5, "center_y":0.75},
        )
        self.terms_input.bind(text=self.calculate)
        self.interest_input = InterestValueInput(
            helper_text=self.appLanguage[self.lang]["interest"],
            input_filter="float",
            write_tab=False,
            multiline=False,
            halign="left",
            size_hint=(0.3, 1),
            pos_hint={"center_x": 0.5, "center_y":0.68},
        )
        self.interest_input.bind(text=self.calculate)

        self.screen.add_widget(self.loan_input)
        self.screen.add_widget(self.terms_input)
        self.screen.add_widget(self.interest_input)

        self.payment_per_month = OutputValue(
            helper_text=self.appLanguage[self.lang]["monthlypayment"],
            size_hint=(0.3, 1),
            pos_hint={"center_x": -1, "center_y": 0.56},
        )
        self.interest_a_day = OutputValue(
            helper_text=self.appLanguage[self.lang]["interestday"],
            size_hint=(0.3, 1),
            pos_hint={"center_x": -1, "center_y": 0.49},
        )
        self.interest_hole_period = OutputValue(
            helper_text=self.appLanguage[self.lang]["interestperiod"],
            size_hint=(0.3, 1),
            pos_hint={"center_x": -1, "center_y": 0.42},
        )
        self.payment_hole_period = OutputValue(
            helper_text=self.appLanguage[self.lang]["paymentperiod"],
            size_hint=(0.3, 1),
            pos_hint={"center_x": -1, "center_y": 0.35},
        )

        self.screen.add_widget(self.payment_per_month)
        self.screen.add_widget(self.interest_a_day)
        self.screen.add_widget(self.interest_hole_period)
        self.screen.add_widget(self.payment_hole_period)
        return self.screen
    

if __name__ == '__main__':
    DebtCounterApp().run()
