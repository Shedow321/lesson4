# вставлення потрібних бібліотек
from colorama import init, Fore, Back, Style
from rich.console import Console
from rich.table import Table

# Робимо так щоб кольори автоматично скидалися після кожного рядка
init(autoreset=True)

# Для кольорового тексту
def colored_text(text: str, color: str = "RED") -> str:
    
    color_dict = {
        "RED": Fore.RED,
        "GREEN": Fore.GREEN,
        "YELLOW": Fore.YELLOW,
        "BLUE": Fore.BLUE,
        "MAGENTA": Fore.MAGENTA,
        "CYAN": Fore.CYAN,
        "WHITE": Fore.WHITE
    }
    return color_dict.get(color.upper(), Fore.WHITE) + text


# Вивід тексту з кольоровим фоном
def print_colored_background(text: str, bg_color: str = "YELLOW") -> None:
    
    bg_dict = {
        "RED": Back.RED,
        "GREEN": Back.GREEN,
        "YELLOW": Back.YELLOW,
        "BLUE": Back.BLUE,
        "MAGENTA": Back.MAGENTA,
        "CYAN": Back.CYAN,
        "WHITE": Back.WHITE
    }
    print(bg_dict.get(bg_color.upper(), Back.RESET) + text + Style.RESET_ALL)


# Створяння та показ таблиці
def print_table(title_color: str = "CYAN", math_color: str = "MAGENTA", physics_color: str = "GREEN") -> None:
   
    console = Console()
    table = Table(title="Таблиця оцінок")

    table.add_column("Ім’я", justify="left", style=title_color.lower(), no_wrap=True)
    table.add_column("Математика", justify="center", style=math_color.lower())
    table.add_column("Фізика", justify="center", style=physics_color.lower())

    # Додаємо рядки
    table.add_row("Аня", "12", "14")
    table.add_row("Богдан", "15", "16")
    table.add_row("Катя", "14", "15")

    console.print(table)


# Основа
if __name__ == "__main__":
    # Виклик кольорових функцій
    print(colored_text("Цей текст червоний", "RED"))
    print_colored_background("Тло жовте", "YELLOW")

    # Виводимо таблицю з кольоровими стовпцями
    print_table("cyan", "magenta", "green")

    # Відомі фрази
    print(colored_text("Без праці не виловиш і рибку зі ставка", "BLUE"))
    print_colored_background("Пані Олена", "GREEN")
    print(colored_text("Бажаю успіхів у навчанні!", "MAGENTA"))
    print_colored_background("Amor", "CYAN")
