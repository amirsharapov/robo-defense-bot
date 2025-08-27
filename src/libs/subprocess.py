import subprocess
from dataclasses import dataclass


@dataclass
class ExecCmdResponse:
    cmd: str
    did_communicate: bool
    process: subprocess.Popen

    stdout: str = None
    stderr: str = None

    @property
    def returncode(self):
        return self.process.returncode



def execute_command(command: str):
    return exec_cmd(command, wait=True)
    # try:
    #     result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
    #     return result.stdout.strip()
    # except subprocess.CalledProcessError as e:
    #     raise RuntimeError(f"Command '{command}' failed with error: {e.stderr.strip()}") from e


def exec_cmd(cmd: str, wait: bool, strip_output: bool = True) -> ExecCmdResponse:
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )

    if not wait:
        return ExecCmdResponse(
            cmd=cmd,
            did_communicate=False,
            process=process
        )

    process.wait()

    stdout, stderr = process.communicate(timeout=5)

    if strip_output:
        if stdout:
            stdout = stdout.strip()
        if stderr:
            stderr = stderr.strip()

    if process.returncode != 0 or stderr:
        raise RuntimeError(f"Command '{cmd}' failed with error: {stderr}")

    return ExecCmdResponse(
        cmd=cmd,
        did_communicate=True,
        process=process,
        stdout=stdout,
        stderr=stderr
    )
