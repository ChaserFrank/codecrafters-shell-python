import os
import sys
import subprocess

BUILTINS = {"echo", "exit", "type", "pwd", "cd"}

def find_executable(command):
    path_env = os.environ.get("PATH", "")

    for directory in path_env.split(os.pathsep):
        full_path = os.path.join(directory, command)

        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path

    return None

def main():
    while True:
        # Display prompt
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Captures the user's command in the "command" variable
        command = input()
        parts = command.split()

        if not parts:
            continue

        # Exit the shell
        if parts[0] == "exit":
            break

        elif parts[0] == "echo":
            print(" ".join(parts[1:]))

        elif parts[0] == "pwd":
            print(os.getcwd())

        elif parts[0] == "cd":
            directory = parts[1]

            if directory == "~":
                directory = os.getenv("HOME", "")

            try:
                os.chdir(directory)
            except FileNotFoundError:
                print(f"cd: {directory}: No such file or directory")

        elif parts[0] == "type":
             cmd = parts[1]

             if cmd in BUILTINS:
                 print(f"{cmd} is a shell builtin")
             else:
                 executable = find_executable(cmd)

                 if executable:
                     print(f"{cmd} is {executable}")
                 else:
                     print(f"{cmd}: not found")

       # executable + unknown command
        else:
            executable = find_executable(parts[0])
            if executable:
                subprocess.run(
                    [parts[0]] + parts[1:],
                    executable=executable
                )
            else:
                # Prints the "<command>: command not found" message
                print(f"{command}: command not found")

if __name__ == "__main__":
    main()