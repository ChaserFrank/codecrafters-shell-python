import sys


def main():
    builtins = {"echo", "exit", "type"}

    while True:
        # Display prompt
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Captures the user's command in the "command" variable
        command = input()
        parts = command.split(" ")

        if not parts:
            continue

        # Exit the shell
        if parts[0] == "exit":
            break

        elif parts[0] == "echo":
            print(" ".join(parts[1:]))

        elif parts[0] == "type":
            if len(parts) > 1:
                cmd = parts[1]

                if cmd in builtins:
                    print(f"{cmd} is a shell builtin")
                else:
                    print(f"{cmd} not found")

        else:
            # Prints the "<command>: command not found" message
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()