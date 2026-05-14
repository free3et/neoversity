from helpers import parse_input, add_contact, change_contact, show_phone, show_all
from colorama import Fore, Style

def main():
    contacts = {}
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
            print(f"{Fore.GREEN}{add_contact(args, contacts)}{Style.RESET_ALL}")

        elif command == "change":
            print(f"{Fore.YELLOW}{change_contact(args, contacts)}{Style.RESET_ALL}")

        elif command == "phone":
            print(f"{Fore.YELLOW}{show_phone(args, contacts)}{Style.RESET_ALL}")

        elif command == "all":
            print(f"{Fore.BLUE}{show_all(contacts)}{Style.RESET_ALL}")

        else:
            print(f"{Fore.RED}Invalid command ❌.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
