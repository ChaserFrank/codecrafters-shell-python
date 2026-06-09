import sys


def main():
    while True:
        # Display prompt
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Captures the user's command in the "command" variable
        command = input()

        # Exit the shell
        if command == "exit":
            break

        if command.startswith("echo"):
            print(command)

        # Prints the "<command>: command not found" message
        print(f"{command}: command not found")


if __name__ == "__main__":
    main()