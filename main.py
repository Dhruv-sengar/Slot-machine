from colorama import Fore, Style
import random

MIN_BET = 1
MAX_BET = 100
MAX_LINES = 3

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, count in symbols.items():
        all_symbols.extend([symbol] * count)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)

    return columns

def print_slot_machine(columns):
    for row in range(len(columns[0])):
        row_symbols = []
        for column in columns:
            row_symbols.append(column[row])
        print(" | ".join(Fore.GREEN + symbol + Style.RESET_ALL for symbol in row_symbols))

def deposit():
    while True:
        amount = input(Fore.RED + "What would you like to deposit? ₹" + Fore.RESET)
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print(Fore.RED + "Invalid amount. Amount must be greater than 0." + Fore.RESET)
        else:
            print(Fore.RED + "Invalid amount. Please enter a valid integer." + Fore.RESET)
    return amount

def get_number_of_lines():
    while True:
        lines = input(Fore.RED + "Enter the number of lines to bet on (1-" + str(MAX_LINES) + "): " + Fore.RESET)
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print(Fore.RED + "Invalid number of lines. Please enter a number between 1 and " + str(MAX_LINES) + "." + Fore.RESET)
        else:
            print(Fore.RED + "Invalid input. Please enter a valid integer." + Fore.RESET)
    return lines

def get_bet():
    while True:
        bet = input(Fore.RED + "How much would you like to bet on each line? ₹" + Fore.RESET)
        if bet.isdigit():
            bet = int(bet)
            if MIN_BET <= bet <= MAX_BET:
                break
            else:
                print(Fore.RED + f"Invalid bet amount. Bet must be between ₹{MIN_BET} and ₹{MAX_BET}." + Fore.RESET)
        else:
            print(Fore.RED + "Invalid bet. Please enter a valid integer." + Fore.RESET)
    return bet

def calculate_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            if column[line] != symbol:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
    return winnings, winning_lines

def main():
    balance = deposit()
    while True:
        lines = get_number_of_lines()
        bet = get_bet()
        total_bet = bet * lines
        if total_bet > balance:
            print(Fore.RED + f"Insufficient funds. You only have ₹{balance}. Please deposit more." + Fore.RESET)
        else:
            print(Fore.YELLOW + f"Betting on {lines} lines for ₹{bet} each. Total bet is ₹{total_bet}." + Fore.RESET)

            slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
            print_slot_machine(slots)

            winnings, winning_lines = calculate_winnings(slots, lines, bet, symbol_value)
            print(Fore.YELLOW + f"You won ₹{winnings}." + Fore.RESET)
            if winning_lines:
                print(Fore.GREEN + f"Winning lines: {', '.join(map(str, winning_lines))}" + Fore.RESET)
            else:
                print(Fore.RED + "No winning lines." + Fore.RESET)

            balance += winnings - total_bet
            print(Fore.CYAN + f"Your new balance is ₹{balance}." + Fore.RESET)

            if balance <= 0:
                print(Fore.RED + "You have run out of funds. Game over!" + Fore.RESET)
                break

            response = input(Fore.BLUE + "Would you like to keep betting or quit? (Enter 'q' to quit or any other key to continue): " + Fore.RESET)
            if response.lower() == 'q':
                break

    print(Fore.CYAN + f"You ended the game with a balance of ₹{balance}." + Fore.RESET)

if __name__ == "__main__":
    main()
