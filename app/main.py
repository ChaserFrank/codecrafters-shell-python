import sys


def main():
    sys.stdout.write("$ ")
    pass

    # Captures the user's command in the "command" variable
    command = input()

    # Prints the "<command>: command not found" message
    print(f"{command}: command not found")


if __name__ == "__main__":
    main()
