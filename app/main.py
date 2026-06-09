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

        parts = command.split(" ")

        if len(parts) > 0 and parts[0] == "echo":
            # Prints the arguments passed to the "echo" command
            print(" ".join(parts[1:]))

        else:
            # Prints the "<command>: command not found" message
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()