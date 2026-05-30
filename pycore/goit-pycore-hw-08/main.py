from helpers import load_data, parse_input, add_contact, change_contact, save_data, show_phone, show_all, add_birthday, show_birthday, birthdays
from colorama import Fore, Style

def main():
    book = load_data()
    print("Welcome to the assistant bot 🤖!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print(f"{Fore.MAGENTA}Good bye!{Style.RESET_ALL}")
            break
        
        elif command == "hello":
            print(f"{Fore.MAGENTA}Hello 👋! How can I help you?{Style.RESET_ALL}")

        elif command == "add":
            print(f"{Fore.GREEN}{add_contact(args, book)}{Style.RESET_ALL}")

        elif command == "change":
            print(f"{Fore.YELLOW}{change_contact(args, book)}{Style.RESET_ALL}")

        elif command == "phone":
            print(f"{Fore.YELLOW}{show_phone(args, book)}{Style.RESET_ALL}")

        elif command == "all":
            print(f"{Fore.BLUE}{show_all(book)}{Style.RESET_ALL}")

        elif command == "add-birthday":
            print(f"{Fore.GREEN}{add_birthday(args, book)}{Style.RESET_ALL}")

        elif command == "show-birthday":
            print(f"{Fore.LIGHTRED_EX}{show_birthday(args, book)}{Style.RESET_ALL}")

        elif command == "birthdays":
            print(f"{Fore.LIGHTRED_EX}{birthdays(args, book)}{Style.RESET_ALL}")

        else:
            print(f"{Fore.RED}Invalid command ❌.{Style.RESET_ALL}")
        
    save_data(book)

if __name__ == "__main__":
    main()
