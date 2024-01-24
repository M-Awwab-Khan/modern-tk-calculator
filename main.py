import tkinter as tk
from constants import *
import math

class Calculator:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.geometry("600x667")
        self.window.resizable(0, 0)
        self.window.title("Calculator")
        self.digits = {
            7:(1, 1), 8:(1, 2), 9:(1, 3),
            4:(2, 1), 5:(2, 2), 6:(2, 3),
            1:(3, 1), 2:(3, 2), 3:(3, 3),
            '.': (4, 2), 0:(4, 1)
        }

        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

        self.total_expression = ""
        self.current_expression = ""

        self.display_frame = self.create_display_frame()
        self.buttons_frame = self.create_buttons_frame()
        self.total_label, self.label = self.create_display_labels()
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

        for x in range(5):
            self.buttons_frame.rowconfigure(x, weight=1)
        for x in range(1, 8):
            self.buttons_frame.columnconfigure(x, weight=1)
        
    def bind_keys(self):
        self.window.bind('<Return>', lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))
        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))
    
    def create_special_buttons(self):
        tk.Button(self.buttons_frame, text="C", font=DEFAULT_FONT_STYLE, bg=OFF_WHITE, fg=LABEL_COLOR, borderwidth=0, command=self.clear).grid(row=0, column=1, sticky=tk.NSEW)
        tk.Button(self.buttons_frame, text="=", font=DEFAULT_FONT_STYLE, bg=LIGHT_BLUE, fg=LABEL_COLOR, borderwidth=0, command=self.evaluate).grid(row=4, column=6, columnspan=2, sticky=tk.NSEW)
        tk.Button(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.sqrt).grid(row=0, column=3, sticky=tk.NSEW)
        tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.square).grid(row=0, column=2, sticky=tk.NSEW)
        tk.Button(self.buttons_frame, text="sin", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.sine).grid(row=0, column=4, sticky=tk.NSEW)
        tk.Button(self.buttons_frame, text="cos", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.cos).grid(row=1, column=4, sticky=tk.NSEW)
        tk.Button(self.buttons_frame, text="tan", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.tan).grid(row=2, column=4, sticky=tk.NSEW)
        tk.Button(self.buttons_frame, text="\u33d1", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.ln).grid(row=3, column=4, sticky=tk.NSEW)
        tk.Button(self.buttons_frame, text="\u03c0", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.pi).grid(row=4, column=4, sticky=tk.NSEW)
        tk.Button(self.buttons_frame, text="\u2107", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.e).grid(row=4, column=3, sticky=tk.NSEW)
        tk.Button(self.buttons_frame, text="sin⁻¹x", bg=OFF_WHITE, fg=LABEL_COLOR, font=SMALL_FONT_STYLE, borderwidth=0, command=self.arcsin).grid(row=0, column=5, sticky=tk.NSEW)
        tk.Button(self.buttons_frame, text="cos⁻¹x", bg=OFF_WHITE, fg=LABEL_COLOR, font=SMALL_FONT_STYLE, borderwidth=0, command=self.arccos).grid(row=1, column=5, sticky=tk.NSEW)
        tk.Button(self.buttons_frame, text="tan⁻¹x", bg=OFF_WHITE, fg=LABEL_COLOR, font=SMALL_FONT_STYLE, borderwidth=0, command=self.arctan).grid(row=2, column=5, sticky=tk.NSEW)
        tk.Button(self.buttons_frame, text="x!", bg=OFF_WHITE, fg=LABEL_COLOR, font=SMALL_FONT_STYLE, borderwidth=0, command=self.fact).grid(row=3, column=5, sticky=tk.NSEW)
        tk.Button(self.buttons_frame, text="|x|", bg=OFF_WHITE, fg=LABEL_COLOR, font=SMALL_FONT_STYLE, borderwidth=0, command=self.absolute).grid(row=4, column=5, sticky=tk.NSEW)
        tk.Button(self.buttons_frame, text="x⁻¹", bg=OFF_WHITE, fg=LABEL_COLOR, font=SMALL_FONT_STYLE, borderwidth=0, command=self.inverse).grid(row=0, column=6, sticky=tk.NSEW)
        tk.Button(self.buttons_frame, text="xⁿ", bg=OFF_WHITE, fg=LABEL_COLOR, font=SMALL_FONT_STYLE, borderwidth=0, command=self.power).grid(row=1, column=6, sticky=tk.NSEW)
        tk.Button(self.buttons_frame, text="eˣ", bg=OFF_WHITE, fg=LABEL_COLOR, font=SMALL_FONT_STYLE, borderwidth=0, command=self.exp).grid(row=2, column=6, sticky=tk.NSEW)
        tk.Button(self.buttons_frame, text="mod", bg=OFF_WHITE, fg=LABEL_COLOR, font=SMALL_FONT_STYLE, borderwidth=0, command=self.mod).grid(row=3, column=6, sticky=tk.NSEW)




    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE, borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)
    
    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, font=DEFAULT_FONT_STYLE, bg=OFF_WHITE, fg=LABEL_COLOR, borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=7, sticky=tk.NSEW)
            i += 1

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()
    
    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill="both")

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill="both")

        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill='both')
        return frame
    
    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()


    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression} ** (1/2)"))
        self.update_label()

    def square(self):
        self.current_expression = str(eval(f"{self.current_expression} ** 2"))
        self.update_label()

    def sine(self):
        self.current_expression = str(math.sin(float(self.current_expression)))
        self.update_label()

    def arcsin(self):
        self.current_expression = str(math.asin(float(self.current_expression)))
        self.update_label()

    def arccos(self):
        self.current_expression = str(math.acos(float(self.current_expression)))
        self.update_label()

    def arctan(self):
        self.current_expression = str(math.atan(float(self.current_expression)))
        self.update_label()

    def cos(self):
        self.current_expression = str(math.cos(float(self.current_expression)))
        self.update_label()

    def tan(self):
        self.current_expression = str(math.tan(float(self.current_expression)))
        self.update_label()

    def e(self):
        self.current_expression = str(math.e)
        self.update_label()
   
    def pi(self):
        self.current_expression = str(math.pi)
        self.update_label()

    def ln(self):
        self.current_expression = str(math.log(float(self.current_expression)))
        self.update_label()
        
    def fact(self):
        self.current_expression = str(math.factorial(int(self.current_expression)))
        self.update_label()

    def absolute(self):
        self.current_expression = str(abs(float(self.current_expression)))
        self.update_label()

    def inverse(self):
        self.current_expression = str(1/int(self.current_expression))
        self.update_label()

    def power(self):
        self.current_expression += '**'
        self.update_label()

    def exp(self):
        self.current_expression = str(math.exp(float(self.current_expression)))
        self.update_label()

    def mod(self):
        self.current_expression += '%'
        self.update_label()

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))
        except Exception:
            self.current_expression = 'Error'
        finally:
            self.update_label()
            self.total_expression = ""


    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()


    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame
    
    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:11])
    
    def run(self):
        self.window.mainloop()
    
if __name__ == "__main__":
    calc = Calculator()
    calc.run()