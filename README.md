[![progress-banner](https://backend.codecrafters.io/progress/shell/a215f8a9-3852-4b5f-b1d6-f4909c2db627)](https://app.codecrafters.io/users/ChaserFrank?r=2qF)

# Python Shell Implementation

This is a Python implementation of a POSIX-compliant shell, built as part of the
["Build Your Own Shell" Challenge](https://app.codecrafters.io/courses/shell/overview).

In this project, you'll learn about shell command parsing, REPLs, builtin commands, command execution, and I/O redirection.

**Note**: If you're viewing this repo on GitHub, head over to
[codecrafters.io](https://codecrafters.io) to try the challenge.

## Features Implemented

### Core Shell Features
- ✅ Interactive REPL (Read-Eval-Print Loop) with prompt (`$`)
- ✅ Tab completion support for commands
- ✅ Command parsing using shell-like syntax (handles quoted strings, escapes)

### Builtin Commands
The following builtin commands are implemented:

1. **echo** - Display text
   - Usage: `echo [text]`
   - Outputs the provided text to stdout

2. **pwd** - Print working directory
   - Usage: `pwd`
   - Displays the current working directory

3. **cd** - Change directory
   - Usage: `cd [directory]`
   - Supports `~` for home directory
   - Shows error message if directory doesn't exist

4. **type** - Display command type
   - Usage: `type [command]`
   - Shows if a command is a builtin or external executable
   - Displays the path to external executables
   - Shows "not found" if command doesn't exist

5. **exit** - Exit the shell
   - Usage: `exit`
   - Cleanly terminates the shell

### External Commands
- ✅ Command resolution via PATH environment variable
- ✅ Execution of external programs with arguments
- ✅ Proper executable permission checking

### I/O Redirection
The shell supports the following redirection operators:

- **Stdout Redirection:**
  - `command > file` - Write stdout to file (overwrite)
  - `command 1> file` - Equivalent to `>`
  - `command >> file` - Append stdout to file
  - `command 1>> file` - Equivalent to `>>`

- **Stderr Redirection:**
  - `command 2> file` - Write stderr to file (overwrite)
  - `command 2>> file` - Append stderr to file

- **Combined:** Redirection operators can be used with any command (builtin or external)

## Project Structure

```
app/
├── main.py          # Main shell implementation
```

## Getting Started

### Prerequisites
- Python 3.x
- `uv` package manager

### Running the Shell

```sh
./your_program.sh
```

Or directly:

```sh
python app/main.py
```

### Example Usage

```sh
$ echo Hello, World!
Hello, World!

$ pwd
/home/user/projects

$ cd ~
$ pwd
/home/user

$ type echo
echo is a shell builtin

$ type ls
ls is /usr/bin/ls

$ echo "Hello" > output.txt
$ cat output.txt
Hello

$ echo "Appended" >> output.txt
```

## Testing & Submission

To run tests:

```sh
codecrafters submit
```

## Architecture

The shell implementation follows this flow:

1. **Display Prompt** - Shows `$` prompt
2. **Read Input** - Gets user command with readline support
3. **Parse Command** - Uses `shlex.split()` to parse the command line
4. **Parse Redirection** - Identifies and extracts redirection operators
5. **Execute Command** - Routes to builtin or external command handler
6. **Handle I/O** - Redirects output to files as specified

### Key Functions

- `find_executable(command)` - Searches PATH for executable
- `completer(text, state)` - Provides tab completion suggestions
- `main()` - Main REPL loop handling all shell operations

## Limitations & Future Work

- [ ] Pipes (`|`) - Connect output of one command to another
- [ ] Command substitution (`` `command` `` or `$(command)`)
- [ ] Variable expansion (e.g., `$HOME`, `$PATH`)
- [ ] Wildcards and globbing (`*`, `?`, `[...]`)
- [ ] Job control (background processes with `&`)
- [ ] More complex redirection (e.g., `2>&1`)
- [ ] Script files support
- [ ] Aliases and functions
- [ ] History navigation

## Notes

- The shell uses Python's `subprocess` module for executing external commands
- Tab completion currently supports: `echo`, `exit`
- The implementation handles both quoted and unquoted arguments correctly
```
