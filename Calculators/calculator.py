"""
╔══════════════════════════════════════════════╗
║         🔥 PYTHON CALCULATOR 🔥             ║
║         by kotan123                          ║
╚══════════════════════════════════════════════╝

A powerful terminal calculator with:
  - Basic & advanced math operations
  - Expression evaluation with parentheses
  - Calculation history
  - Beautiful colored UI
"""

import math
import os
import sys

# ─── ANSI Colors ───────────────────────────────────────────
class Colors:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    DIM     = "\033[2m"
    BG_BLUE = "\033[44m"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
    ██████╗ █████╗ ██╗      ██████╗
   ██╔════╝██╔══██╗██║     ██╔════╝
   ██║     ███████║██║     ██║
   ██║     ██╔══██║██║     ██║
   ╚██████╗██║  ██║███████╗╚██████╗
    ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝
{Colors.RESET}
{Colors.YELLOW}  ⚡ Python Calculator v1.0 — by kotan123 ⚡{Colors.RESET}
{Colors.DIM}  ─────────────────────────────────────────{Colors.RESET}
"""
    print(banner)


def print_menu():
    menu = f"""
{Colors.GREEN}{Colors.BOLD}  ┌─────────── OPERATIONS ───────────┐{Colors.RESET}
{Colors.GREEN}  │                                   │
  │  {Colors.WHITE}[1]{Colors.GREEN}  ➕  Add                      │
  │  {Colors.WHITE}[2]{Colors.GREEN}  ➖  Subtract                 │
  │  {Colors.WHITE}[3]{Colors.GREEN}  ✖️   Multiply                 │
  │  {Colors.WHITE}[4]{Colors.GREEN}  ➗  Divide                   │
  │  {Colors.WHITE}[5]{Colors.GREEN}  📐  Power (x^y)              │
  │  {Colors.WHITE}[6]{Colors.GREEN}  √   Square Root              │
  │  {Colors.WHITE}[7]{Colors.GREEN}  📊  Percentage               │
  │  {Colors.WHITE}[8]{Colors.GREEN}  🔢  Factorial                │
  │  {Colors.WHITE}[9]{Colors.GREEN}  📝  Expression Mode          │
  │  {Colors.WHITE}[H]{Colors.GREEN}  📜  History                  │
  │  {Colors.WHITE}[C]{Colors.GREEN}  🧹  Clear Screen             │
  │  {Colors.WHITE}[Q]{Colors.GREEN}  🚪  Quit                     │
  │                                   │
  └───────────────────────────────────┘{Colors.RESET}
"""
    print(menu)


def get_number(prompt):
    while True:
        try:
            value = input(f"{Colors.CYAN}  {prompt}: {Colors.WHITE}")
            print(Colors.RESET, end="")
            return float(value)
        except ValueError:
            print(f"{Colors.RED}  ✘ Invalid number, try again.{Colors.RESET}")


def display_result(expression, result):
    print()
    print(f"{Colors.MAGENTA}  ┌──────────── RESULT ────────────┐{Colors.RESET}")
    print(f"{Colors.MAGENTA}  │{Colors.RESET}  {Colors.DIM}{expression}{Colors.RESET}")
    print(f"{Colors.MAGENTA}  │{Colors.RESET}")
    if result == int(result):
        result = int(result)
    print(f"{Colors.MAGENTA}  │{Colors.RESET}  {Colors.BOLD}{Colors.YELLOW}= {result}{Colors.RESET}")
    print(f"{Colors.MAGENTA}  └─────────────────────────────────┘{Colors.RESET}")
    print()
    return f"  {expression} = {result}"


def safe_eval(expr):
    """Safely evaluate a math expression."""
    allowed_names = {
        "abs": abs, "round": round,
        "sin": math.sin, "cos": math.cos, "tan": math.tan,
        "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
        "pi": math.pi, "e": math.e,
        "pow": pow, "floor": math.floor, "ceil": math.ceil,
    }
    for char in expr:
        if char not in "0123456789+-*/().% abcdefghijklmnopqrstuvwxyz,^":
            raise ValueError(f"Forbidden character: {char}")
    expr = expr.replace("^", "**")
    code = compile(expr, "<string>", "eval")
    for name in code.co_names:
        if name not in allowed_names:
            raise NameError(f"Use of '{name}' is not allowed")
    return eval(code, {"__builtins__": {}}, allowed_names)


def operation_add(history):
    a = get_number("Enter first number")
    b = get_number("Enter second number")
    result = a + b
    h = display_result(f"{a} + {b}", result)
    history.append(h)


def operation_subtract(history):
    a = get_number("Enter first number")
    b = get_number("Enter second number")
    result = a - b
    h = display_result(f"{a} - {b}", result)
    history.append(h)


def operation_multiply(history):
    a = get_number("Enter first number")
    b = get_number("Enter second number")
    result = a * b
    h = display_result(f"{a} * {b}", result)
    history.append(h)


def operation_divide(history):
    a = get_number("Enter first number")
    b = get_number("Enter second number")
    if b == 0:
        print(f"\n{Colors.RED}  ✘ Error: Division by zero!{Colors.RESET}\n")
        return
    result = a / b
    h = display_result(f"{a} / {b}", result)
    history.append(h)


def operation_power(history):
    a = get_number("Enter base")
    b = get_number("Enter exponent")
    result = a ** b
    h = display_result(f"{a} ^ {b}", result)
    history.append(h)


def operation_sqrt(history):
    a = get_number("Enter number")
    if a < 0:
        print(f"\n{Colors.RED}  ✘ Error: Cannot take square root of negative number!{Colors.RESET}\n")
        return
    result = math.sqrt(a)
    h = display_result(f"sqrt({a})", result)
    history.append(h)


def operation_percentage(history):
    a = get_number("Enter number")
    b = get_number("Enter percentage")
    result = a * b / 100
    h = display_result(f"{b}% of {a}", result)
    history.append(h)


def operation_factorial(history):
    a = get_number("Enter a non-negative integer")
    if a < 0 or a != int(a):
        print(f"\n{Colors.RED}  ✘ Error: Factorial requires a non-negative integer!{Colors.RESET}\n")
        return
    result = math.factorial(int(a))
    h = display_result(f"{int(a)}!", result)
    history.append(h)


def expression_mode(history):
    print(f"\n{Colors.BLUE}  📝 Expression Mode{Colors.RESET}")
    print(f"{Colors.DIM}  Available: +, -, *, /, ^, (), sin, cos, tan, sqrt, log, pi, e{Colors.RESET}")
    print(f"{Colors.DIM}  Type 'back' to return to menu{Colors.RESET}\n")
    while True:
        expr = input(f"{Colors.CYAN}  >>> {Colors.WHITE}").strip()
        print(Colors.RESET, end="")
        if expr.lower() == "back":
            break
        if not expr:
            continue
        try:
            result = safe_eval(expr)
            h = display_result(expr, result)
            history.append(h)
        except Exception as e:
            print(f"{Colors.RED}  ✘ Error: {e}{Colors.RESET}\n")


def show_history(history):
    print(f"\n{Colors.BLUE}{Colors.BOLD}  ┌──────────── HISTORY ───────────┐{Colors.RESET}")
    if not history:
        print(f"{Colors.DIM}  │  No calculations yet.          │{Colors.RESET}")
    else:
        for i, entry in enumerate(history, 1):
            print(f"{Colors.BLUE}  │{Colors.RESET} {Colors.DIM}{i}.{Colors.RESET}{entry}")
    print(f"{Colors.BLUE}  └─────────────────────────────────┘{Colors.RESET}\n")


def main():
    history = []
    clear_screen()
    print_banner()

    operations = {
        "1": operation_add,
        "2": operation_subtract,
        "3": operation_multiply,
        "4": operation_divide,
        "5": operation_power,
        "6": operation_sqrt,
        "7": operation_percentage,
        "8": operation_factorial,
    }

    while True:
        print_menu()
        choice = input(f"{Colors.YELLOW}  Choose an option ▶ {Colors.WHITE}").strip().upper()
        print(Colors.RESET, end="")

        if choice == "Q":
            print(f"\n{Colors.CYAN}  👋 Goodbye! Thanks for using Python Calculator.{Colors.RESET}\n")
            sys.exit(0)
        elif choice == "C":
            clear_screen()
            print_banner()
        elif choice == "H":
            show_history(history)
        elif choice == "9":
            expression_mode(history)
        elif choice in operations:
            operations[choice](history)
        else:
            print(f"\n{Colors.RED}  ✘ Invalid option. Try again.{Colors.RESET}\n")


if __name__ == "__main__":
    main()
