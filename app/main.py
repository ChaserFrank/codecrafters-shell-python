import os
import sys
import subprocess
import shlex
import readline

BUILTINS = {"echo", "exit", "type", "pwd", "cd", "complete", "jobs", "history"}
BUILTIN_COMPLETIONS = sorted(BUILTINS)

COMPLETIONS = {}
HISTORY = []

JOBS = []

def find_executable(command):
    path_env = os.environ.get("PATH", "")

    for directory in path_env.split(os.pathsep):
        full_path = os.path.join(directory, command)

        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path

    return None

def get_executables():
    executables = set()

    path_env = os.environ.get("PATH", "")

    for directory in path_env.split(os.pathsep):

        if not os.path.isdir(directory):
            continue

        try:
            for file in os.listdir(directory):
                full_path = os.path.join(directory, file)

                if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                    executables.add(file)

        except OSError:
            pass

    return executables

def completer(text, state):
    line = readline.get_line_buffer()
    words = line.split()

    # Command completion
    if " " not in line:
        commands = BUILTIN_COMPLETIONS + list(get_executables())

        matches = sorted(
            cmd for cmd in set(commands)
            if cmd.startswith(text)
        )

        if state >= len(matches):
            return None

        match = matches[state]

        if len(matches) == 1:
            match += " "

        return match

    # Programmable completion
    if words and words[0] in COMPLETIONS:
        command = words[0]

        # Determine current word and previous word
        if line.endswith(" "):
            current_word = ""

            if len(words) >= 2:
                previous_word = words[-1]
            else:
                previous_word = ""
        else:
            current_word = words[-1]

            if len(words) >= 2:
                previous_word = words[-2]
            else:
                previous_word = ""

        try:
            env = os.environ.copy()

            env["COMP_LINE"] = line
            env["COMP_POINT"] = str(len(line))

            result = subprocess.run(
                [
                    COMPLETIONS[command],
                    command,
                    current_word,
                    previous_word,
                ],
                capture_output=True,
                text=True,
                env=env
            )

            matches = [
                candidate.strip()
                for candidate in result.stdout.splitlines()
                if candidate.strip()
            ]

        except Exception:
            matches = []

        if state >= len(matches):
            return None

        completion = matches[state]

        if len(matches) == 1:
            completion += " "

        return completion

    # Filename / directory completion
    else:
        if "/" in text:
            directory, prefix = text.rsplit("/", 1)

            search_dir = directory if directory else "."

            try:
                matches = sorted(
                    entry
                    for entry in os.listdir(search_dir)
                    if entry.startswith(prefix)
                )
            except OSError:
                matches = []

            if state >= len(matches):
                return None

            match = matches[state]

            completion = f"{directory}/{match}"

            if os.path.isdir(os.path.join(search_dir, match)):
                completion += "/"
            elif len(matches) == 1:
                completion += " "

            return completion

        else:
            matches = sorted(
                f for f in os.listdir(".")
                if f.startswith(text)
            )

            if state >= len(matches):
                return None

            match = matches[state]

            completion = match

            # Directory -> trailing /
            if os.path.isdir(match):
                completion += "/"

            # File -> trailing space
            elif len(matches) == 1:
                completion += " "

            return completion

def reap_jobs():
    completed_jobs = []

    total_jobs = len(JOBS)

    for i, job in enumerate(JOBS):

        if total_jobs == 1:
            marker = "+"

        elif i == total_jobs - 1:
            marker = "+"

        elif i == total_jobs - 2:
            marker = "-"

        else:
            marker = " "

        if job["process"].poll() is not None:

            print(
                f"[{job['id']}]"
                f"{marker}  "
                f"{'Done':<24}"
                f"{job['command'].removesuffix(' &')}"
            )

            completed_jobs.append(job)

    for job in completed_jobs:
        JOBS.remove(job)

def get_next_job_id():

    used_ids = {job["id"] for job in JOBS}

    job_id = 1

    while job_id in used_ids:
        job_id += 1

    return job_id

def builtin_output(cmd):

    if cmd[0] == "echo":
        return " ".join(cmd[1:]) + "\n"

    elif cmd[0] == "pwd":
        return os.getcwd() + "\n"

    elif cmd[0] == "type":

        target = cmd[1]

        if target in BUILTINS:
            return f"{target} is a shell builtin\n"

        executable = find_executable(target)

        if executable:
            return f"{target} is {executable}\n"

        return f"{target}: not found\n"

    return ""

def main():
    readline.set_completer_delims(" \t\n")
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)

    while True:
        reap_jobs()
        command = input("$ ")

        HISTORY.append(command)

        stdout_file = None
        stderr_file = None

        stdout_mode = "w"
        stderr_mode = "w"

        parts = shlex.split(command)

        background = False

        if parts and parts[-1] == "&":
            background = True
            parts.pop()

        # Handle stdout redirection (> and 1>)
        if ">" in parts:
            idx = parts.index(">")
            stdout_file = parts[idx + 1]
            parts = parts[:idx]

        elif "1>" in parts:
            idx = parts.index("1>")
            stdout_file = parts[idx + 1]
            parts = parts[:idx]

        elif ">>" in parts:
            idx = parts.index(">>")
            stdout_file = parts[idx + 1]
            stdout_mode = "a"
            parts = parts[:idx]

        elif "1>>" in parts:
            idx = parts.index("1>>")
            stdout_file = parts[idx + 1]
            stdout_mode = "a"
            parts = parts[:idx]

        elif "2>>" in parts:
            idx = parts.index("2>>")
            stderr_file = parts[idx + 1]
            stderr_mode = "a"
            parts = parts[:idx]

        # Handle stderr redirection (2>)
        elif "2>" in parts:
            idx = parts.index("2>")
            stderr_file = parts[idx + 1]
            parts = parts[:idx]

        # if "|" in parts:
        #
        #     pipe_index = parts.index("|")
        #
        #     left_cmd = parts[:pipe_index]
        #     right_cmd = parts[pipe_index + 1:]
        #
        #     # builtin | builtin
        #     if left_cmd[0] in BUILTINS and right_cmd[0] in BUILTINS:
        #
        #         print(builtin_output(right_cmd), end="")
        #
        #     # builtin | external
        #     elif left_cmd[0] in BUILTINS:
        #
        #         data = builtin_output(left_cmd)
        #
        #         right_exec = find_executable(right_cmd[0])
        #
        #         if right_exec:
        #             p = subprocess.Popen(
        #                 right_cmd,
        #                 executable=right_exec,
        #                 stdin=subprocess.PIPE,
        #                 text=True
        #             )
        #
        #             p.communicate(data)
        #
        #     # external | builtin
        #     elif right_cmd[0] in BUILTINS:
        #
        #         left_exec = find_executable(left_cmd[0])
        #
        #         if left_exec:
        #             p = subprocess.Popen(
        #                 left_cmd,
        #                 executable=left_exec,
        #                 stdout=subprocess.PIPE,
        #                 text=True
        #             )
        #
        #             # discard pipeline input
        #             p.communicate()
        #
        #         print(builtin_output(right_cmd), end="")
        #
        #     # external | external
        #     else:
        #
        #         left_exec = find_executable(left_cmd[0])
        #         right_exec = find_executable(right_cmd[0])
        #
        #         if left_exec and right_exec:
        #             p1 = subprocess.Popen(
        #                 left_cmd,
        #                 executable=left_exec,
        #                 stdout=subprocess.PIPE
        #             )
        #
        #             p2 = subprocess.Popen(
        #                 right_cmd,
        #                 executable=right_exec,
        #                 stdin=p1.stdout
        #             )
        #
        #             p1.stdout.close()
        #
        #             p2.wait()
        #             p1.wait()
        #
        #     continue

        if "|" in command:

            pipeline_commands = [
                shlex.split(cmd.strip())
                for cmd in command.split("|")
            ]

            # Special case:
            # last command is builtin (needed for: ls | type exit)
            if pipeline_commands[-1][0] in BUILTINS:

                last_cmd = pipeline_commands[-1]

                # Run previous stages and discard output
                if len(pipeline_commands) > 1:

                    processes = []
                    prev_stdout = None

                    for cmd_parts in pipeline_commands[:-1]:

                        executable = find_executable(cmd_parts[0])

                        if not executable:
                            break

                        is_last_external = (
                                cmd_parts == pipeline_commands[-2]
                        )

                        proc = subprocess.Popen(
                            cmd_parts,
                            executable=executable,
                            stdin=prev_stdout,
                            stdout=subprocess.PIPE if is_last_external else subprocess.PIPE,
                            text=True
                        )

                        if prev_stdout:
                            prev_stdout.close()

                        prev_stdout = proc.stdout
                        processes.append(proc)

                    if processes:
                        processes[-1].communicate()

                        for proc in processes[:-1]:
                            proc.wait()

                print(builtin_output(last_cmd), end="")
                continue

            # Normal pipeline (all external commands)
            processes = []
            prev_stdout = None

            for i, cmd_parts in enumerate(pipeline_commands):

                executable = find_executable(cmd_parts[0])

                if not executable:
                    break

                is_last = (i == len(pipeline_commands) - 1)

                proc = subprocess.Popen(
                    cmd_parts,
                    executable=executable,
                    stdin=prev_stdout,
                    stdout=None if is_last else subprocess.PIPE
                )

                if prev_stdout:
                    prev_stdout.close()

                prev_stdout = proc.stdout
                processes.append(proc)

            for proc in processes:
                proc.wait()

            continue

        if not parts:
            continue

        # exit builtin
        if parts[0] == "exit":
            break

        elif parts[0] == "history":

            for index, cmd in enumerate(HISTORY, start=1):
                print(f"{index:>5}  {cmd}")

        elif parts[0] == "jobs":

            completed_jobs = []

            total_jobs = len(JOBS)

            for i, job in enumerate(JOBS):

                if total_jobs == 1:
                    marker = "+"
                elif i == total_jobs - 1:
                    marker = "+"
                elif i == total_jobs - 2:
                    marker = "-"
                else:
                    marker = " "

                if job["process"].poll() is None:

                    print(
                        f"[{job['id']}]"
                        f"{marker}  "
                        f"{'Running':<24}"
                        f"{job['command']}"
                    )

                else:

                    print(
                        f"[{job['id']}]"
                        f"{marker}  "
                        f"{'Done':<24}"
                        f"{job['command'].removesuffix(' &')}"
                    )

                    completed_jobs.append(job)

            for job in completed_jobs:
                JOBS.remove(job)

            continue

        elif parts[0] == "complete":

            # Register completion
            if len(parts) >= 4 and parts[1] == "-C":
                script_path = parts[2]
                command_name = parts[3]

                COMPLETIONS[command_name] = script_path

            # Print completion
            elif len(parts) >= 3 and parts[1] == "-p":
                command_name = parts[2]

                if command_name in COMPLETIONS:
                    print(
                        f"complete -C '{COMPLETIONS[command_name]}' {command_name}"
                    )
                else:
                    print(
                        f"complete: {command_name}: no completion specification"
                    )

            elif parts[1] == "-r":
                command = parts[2]

                COMPLETIONS.pop(command, None)

        # echo builtin
        elif parts[0] == "echo":

            if stderr_file:
                open(stderr_file, stderr_mode).close()
            output = " ".join(parts[1:])

            if stdout_file:
                with open(stdout_file, stdout_mode) as f:
                    print(output, file=f)
            else:
                print(output)

        # pwd builtin
        elif parts[0] == "pwd":

            if stderr_file:
                open(stderr_file, stderr_mode).close()
            output = os.getcwd()

            if stdout_file:
                with open(stdout_file, stdout_mode) as f:
                    print(output, file=f)
            else:
                print(output)

        # cd builtin
        elif parts[0] == "cd":
            directory = parts[1]

            if directory == "~":
                directory = os.getenv("HOME", "")

            try:
                os.chdir(directory)
            except FileNotFoundError:
                print(f"cd: {directory}: No such file or directory")

        # type builtin
        elif parts[0] == "type":

            if stderr_file:
                open(stderr_file, stderr_mode).close()
            cmd = parts[1]

            if cmd in BUILTINS:
                output = f"{cmd} is a shell builtin"
            else:
                executable = find_executable(cmd)

                if executable:
                    output = f"{cmd} is {executable}"
                else:
                    output = f"{cmd}: not found"

            if stdout_file:
                with open(stdout_file, stdout_mode) as f:   print(output, file=f)
            else:
                print(output)

        # External commands
        else:
            executable = find_executable(parts[0])

            if executable:

                if background:
                    job_id = get_next_job_id()
                    process = subprocess.Popen(
                        [parts[0]] + parts[1:],
                        executable=executable
                    )

                    JOBS.append({
                        "id": job_id,
                        "pid": process.pid,
                        "process": process,
                        "command": command,
                    })

                    print(f"[{job_id}] {process.pid}")

                else:
                    # stdout redirected
                    if stdout_file:
                        with open(stdout_file, stdout_mode) as out:
                            subprocess.run(
                                [parts[0]] + parts[1:],
                                executable=executable,
                                stdout=out
                            )

                    # stderr redirected
                    elif stderr_file:
                        with open(stderr_file, stderr_mode) as err:
                            subprocess.run(
                                [parts[0]] + parts[1:],
                                executable=executable,
                                stderr=err
                            )

                    # no redirection
                    else:
                        subprocess.run(
                            [parts[0]] + parts[1:],
                            executable=executable
                        )

            else:
                print(f"{command}: command not found")


if __name__ == "__main__":
    main()