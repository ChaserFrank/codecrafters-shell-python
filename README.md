[![progress-banner](https://backend.codecrafters.io/progress/shell/a215f8a9-3852-4b5f-b1d6-f4909c2db627)](https://app.codecrafters.io/users/ChaserFrank?r=2qF)

# Python Shell Implementation

This is a Python implementation of a POSIX-compliant shell, built as part of the
["Build Your Own Shell" Challenge](https://app.codecrafters.io/courses/shell/overview).

In this project, you'll learn about shell command parsing, REPLs, builtin commands, command execution, I/O redirection, and advanced tab completion.

**Note**: If you're viewing this repo on GitHub, head over to
[codecrafters.io](https://codecrafters.io) to try the challenge.

## Features Implemented

### Core Shell Features
- ✅ Interactive REPL (Read-Eval-Print Loop) with prompt (`$`)
- ✅ Advanced Tab Completion (see details below)
- ✅ Command parsing using shell-like syntax (handles quoted strings, escapes)

### Builtin Commands
The following builtin commands are implemented:

1. **echo** - Display text
2. **pwd** - Print working directory
3. **cd** - Change directory
4. **type** - Display command type
5. **exit** - Exit the shell
6. **complete** - Configure programmable completions

### External Commands
- ✅ Command resolution via PATH environment variable
- ✅ Execution of external programs with arguments

### I/O Redirection
- ✅ Stdout redirection: `>` (overwrite), `>>` (append)
- ✅ Stderr redirection: `2>` (overwrite), `2>>` (append)

## Tab Completion

The shell now features a sophisticated tab completion system:

- **Command Completion**: Completes built-in commands and external executables found in `$PATH`.
- **File/Directory Completion**: Completes file and directory paths in the current directory or based on a partial path.
- **Programmable Completion**: Allows defining custom completion logic for specific commands using the `complete` builtin.

### `complete` Builtin

The `complete` command allows you to register and manage custom completion scripts.

- **Register a completion:**
  ```sh
  complete -C /path/to/script.py command_name
  ```
  The `script.py` will be executed to generate completion suggestions for `command_name`.

- **View a completion:**
  ```sh
  complete -p command_name
  ```

- **Remove a completion:**
  ```sh
  complete -r command_name
  ```

## Project Structure

```
app/
├── main.py          # Main shell implementation
```

## Getting Started

### Prerequisites
- Python 3.x

### Running the Shell

```sh
./your_program.sh
```

Or directly:

```sh
python app/main.py
```

## Testing & Submission

To run tests:

```sh
codecrafters submit
```

## Architecture

The shell implementation follows this flow:

1. **Display Prompt** & **Read Input**
2. **Parse Command** & **Redirection**
3. **Tab Completion**: The `completer` function is invoked by `readline` to provide suggestions based on the current input line. It checks for command, file/directory, or programmable completions.
4. **Execute Command**: Routes to a builtin or external command handler.
5. **Handle I/O**: Redirects output to files as specified.

### Key Functions

- `find_executable(command)`: Searches `$PATH` for an executable.
- `get_executables()`: Returns a set of all executables in `$PATH`.
- `completer(text, state)`: The core logic for all tab completion features.
- `main()`: The main REPL loop.

## Limitations & Future Work

- [ ] Pipes (`|`)
- [ ] Command substitution (`` `command` ``)
- [ ] Variable expansion (`$HOME`, `$PATH`)
- [ ] Job control (`&`)
- [ ] Script file support

## Notes

- The shell uses Python's `subprocess` module for executing external commands and completion scripts.
- The implementation handles both quoted and unquoted arguments correctly.
```
