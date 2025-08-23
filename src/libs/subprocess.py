import subprocess


def execute_command(command: str):
    """
    Executes a shell command and returns the output.

    Args:
        command (str): The command to execute.

    Returns:
        str: The output of the command.
    """
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command '{command}' failed with error: {e.stderr.strip()}") from e
